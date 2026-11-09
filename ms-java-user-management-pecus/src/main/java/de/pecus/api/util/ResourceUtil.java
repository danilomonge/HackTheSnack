package de.pecus.api.util;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import java.util.Properties;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Utileria para acceso a recursos dentro del contexto del proyecto.
 *
 */
public final class ResourceUtil {

    private static final Logger LOGGER = LoggerFactory.getLogger( ResourceUtil.class );

    /**
     * Constructor privado para evitar instanciacion
     */
    private ResourceUtil() {
    }

    /**
     * Se obtiene el classLoader.
     *
     * @return class loader
     */
    public static ClassLoader getClassLoader() {

        ClassLoader classLoader = Thread.currentThread().getContextClassLoader();
        if( classLoader == null ){
            classLoader = ResourceUtil.class.getClassLoader();
        }
        return classLoader;
    }

    /**
     * Method get resources.
     *
     * @param fileName the file name
     * @return resources
     */
    public static List<URL> getResources( String fileName ) {

        ClassLoader classLoader = getClassLoader();
        List<URL> resources = new ArrayList<>();
        try{
            Enumeration<URL> urls = classLoader.getResources( fileName );
            while( urls.hasMoreElements() ){
                resources.add( urls.nextElement() );
            }
        }
        catch( Exception err ){
            resources.add( classLoader.getResource( fileName ) );
        }
        return resources;
    }

    /**
     * Carga uno o mas archivos de propiedades
     *
     * @param fileName the file name
     * @param fileNames the file names
     * @return the properties
     */
    public static Properties loadProperties( String fileName, String... fileNames ) {
    	LOGGER.debug("Cargando properties [fileName]=" + fileName + ", [fileNames]=" + fileNames);
        Properties properties = new Properties();
        try{
            loadProperties( properties, fileName );
        }
        catch( Exception err ){
            properties.clear();
        }
        if( fileNames != null ){
            for( String file : fileNames ){
                loadProperties( properties, file );
            }
        }
        return properties;
    }

    /**
     * Carga un archivo de propiedades
     * 
     * @param properties Objeto properies
     * @param fileName Nombre de archivo
     */
    private static void loadProperties( Properties properties, String fileName ) {
        try{
            List<URL> resources = getResources( fileName );
            for( URL resource : resources ){
                properties.load( resource.openStream() );
            }
        }
        catch( Exception err ){
            properties.clear();
        }
    }

    /**
     * Método para extraer una <code>property</code> de un archivo {@link Properties} especifico.
     * 
     * @param propertyName Nombre de la <code>property</code>.
     * @param propertiesFileName Nombre del archivo {@link Properties}, con la ruta relativa al classpath en tiempo de
     *            ejecución.
     * @return El contenido de la <code>property</code> si fue posible encontrarla o <code>null</code> si no fue
     *         encontrada o el archivo {@link Properties} no pudo ser cargado.
     * @author vn0wosm
     */
    public static String extractProperty( String propertyName, String propertiesFileName ) {
        String extractedProperty = null;
        Properties properties = new Properties();
        InputStream is = Thread.currentThread().getContextClassLoader().getResourceAsStream( propertiesFileName );
        try{
            properties.load( is );
            extractedProperty = properties.getProperty( propertyName );
        }
        catch( IOException e ){
            LOGGER.error( e.getMessage(), e );
        }
        return extractedProperty;
    }

}