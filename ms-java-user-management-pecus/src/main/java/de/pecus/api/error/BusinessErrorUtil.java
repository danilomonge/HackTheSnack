package de.pecus.api.error;

import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Properties;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import de.pecus.api.constant.GeneralConstants;
import de.pecus.api.util.ResourceUtil;
import de.pecus.api.util.ValidatorUtil;

/**
 * Clase de utileria para construccion de objetos de errores de negocio
 * 
 */
public class BusinessErrorUtil {
	
	private static final Logger LOG = LoggerFactory.getLogger(BusinessErrorUtil.class);

    /**
     * Objeto con los properties
     */
	private static Map<String, Map<String, BusinessError>> businessErrorMap = loadProperties();

    private BusinessErrorUtil() {
        throw new IllegalStateException("Utility class");
    }

    private static Map<String, Map<String, BusinessError>> loadProperties() {
    	
    	Map<String, Map<String, BusinessError>> businessErrorIntMap = new HashMap<>();
    	
    	GeneralConstants.IDIOMAS_LIST.forEach((key, value) -> {
    		LOG.info("------- IDIOMAS --------");
    		LOG.info("key: " + key + "value: " + value);
    		String generalConstants = value.split(GeneralConstants.PROPERTY_FILE_SEPARATOR)[0].trim();
    		String architectureError = value.split(GeneralConstants.PROPERTY_FILE_SEPARATOR)[1].trim();
    		String businessError = value.split(GeneralConstants.PROPERTY_FILE_SEPARATOR)[2].trim();
    		Properties propertiesGeneral = ResourceUtil.loadProperties( generalConstants );
    		Properties propertiesArchitecture = ResourceUtil.loadProperties( architectureError );
    		Properties propertiesBusinessError = ResourceUtil.loadProperties( businessError );
    		Map<String, BusinessError> businessErrorMap = new HashMap<>();
    		
    		for( Entry<Object, Object> entry : propertiesGeneral.entrySet() ){
    			String key2 = (String) entry.getKey();
    			String[] value2 = propertiesGeneral.getProperty( key2 ).split( GeneralConstants.PROPERTY_SEPARATOR );
    			LOG.debug("General Error [key2]=" + key2 + "[value2]=" + value2[0] + "-" + value2[1]);
    			businessErrorMap.put( key2, new BusinessError( value2[0].trim(), key2, value2[1].trim() ) );
    		}
    		for( Entry<Object, Object> entry : propertiesArchitecture.entrySet() ){
    			String key2 = (String) entry.getKey();
    			String[] value2 = propertiesArchitecture.getProperty( key2 ).split( GeneralConstants.PROPERTY_SEPARATOR );
    			LOG.debug("Architecture Error [key2]=" + key2 + "[value2]=" + value2[0] + "-" + value2[1]);
    			businessErrorMap.put( key2, new BusinessError( value2[0].trim(), key2, value2[1].trim() ) );
    		}
    		for( Entry<Object, Object> entry : propertiesBusinessError.entrySet() ){
    			String key2 = (String) entry.getKey();
    			String[] value2 = propertiesBusinessError.getProperty( key2 ).split( GeneralConstants.PROPERTY_SEPARATOR );
    			LOG.debug("Business Error [key2]=" + key2 + "[value2]=" + value2[0] + "-" + value2[1]);
    			businessErrorMap.put( key2, new BusinessError( value2[0].trim(), key2, value2[1].trim() ) );
    		}
    		businessErrorIntMap.put(key, businessErrorMap);
    		
    	});
        return businessErrorIntMap;
    }

    /**
     * 
     * Obtiene un error de negocio en cualquier idioma dado de alta a partir del archivo properties
     * 
     * @param name Nombre de error de negocio
     * @param idioma Codigo del idioma ej. es_MX
     * @return Objeto con el error de negocio
     */
    public static BusinessError getBusinessError( String name, String idioma ) {
    	idioma = ValidatorUtil.isNullOrEmpty(idioma) ? GeneralConstants.IDIOMA_EN_US : idioma;
    	if(!ValidatorUtil.isNullOrEmpty(idioma)) {
            boolean idiomaValido = false;
            for(Map.Entry<String, String> idiomaMap : GeneralConstants.IDIOMAS_LIST.entrySet()) {
                if(idiomaMap.getKey().equals(idioma)) {
                    idiomaValido = true;
                }
            }
            if(!idiomaValido) {
                idioma = GeneralConstants.IDIOMA_EN_US;
            }
        }
    	else {
    	    idioma = GeneralConstants.IDIOMA_EN_US;
    	}
    	Map<String, BusinessError> idiomaBusinessError = businessErrorMap.get( idioma );
        return idiomaBusinessError.get( name );
    }

}
