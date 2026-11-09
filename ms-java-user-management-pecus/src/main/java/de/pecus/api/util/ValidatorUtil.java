package de.pecus.api.util;

import java.util.List;
import java.util.Map;

import de.pecus.api.constant.GeneralConstants;
import de.pecus.api.vo.ResponseVO;

/**
 * Clase de utileria para validacion
 * 
 */
public final class ValidatorUtil {

    /**
     * Constructor privado para evitar instanciacion de clase
     */
    private ValidatorUtil() {

    }

    /**
     * Valida si un objeto string es nulo
     *
     * @param obj Objeto a validar
     * @return true si es null
     */
    public static boolean isNull( Object obj ) {
        return obj == null;
    }
    
    /**
     * Valida si un objeto Long es nulo o CERO
     *
     * @param obj Long a validar
     * @return true si es null
     */
    public static boolean isNullOrZero( Long num ) {
        return num == null || num.equals(0L);
    }
    
    /**
     * Valida si un objeto Integer es nulo o CERO
     *
     * @param obj Long a validar
     * @return true si es null
     */
    public static boolean isNullOrZero( Integer num ) {
        return num == null || num == 0;
    }
    
    /**
     * Valida si un objeto Double es nulo o CERO
     *
     * @param obj Long a validar
     * @return true si es null
     */
    public static boolean isNullOrZero( Double num ) {
        return num == null || num.equals(0.0);
    }
    
    /**
     * Valida que la respuesta no contenga errores
     * @param response Objeto de respuesta a evaluar
     * @return True si el objeto respuesta tiene la lista vacia
     */
    public static boolean isSuccessfulResponse(ResponseVO<?> response) {
        return ListUtil.isEmpty(response.getErrors());
    }
    
    /**
     * Valida si un objeto string es nulo o vacio
     *
     * @param str String a validar
     * @return true si str es null o isEmpty
     */
    public static boolean isNullOrEmpty( String str ) {
        return StringUtil.isNullOrEmpty(str);
    }

    
    /**
     * Valida el tamanio minimo de una cadena
     *
     * @param str String a validar
     * @param min int del tamanio minimo de la cadena 
     * @return true si el str cumple el tamanio minimo
     */
    public static boolean minLength( String str, int min ) {
        return str.length() >= min;
    }
    
    /**
     * Valida el tamanio maximo de una cadena
     *
     * @param str String a validar
     * @param min int del tamanio maximo de la cadena 
     * @return true si el str cumple el tamanio maximo
     */
    public static boolean maxLength( String str, int max ) {
        return str.length() <= max;
    }
    
    /**
     * Valida si una lista es nulo o vacia
     *
     * @param list Lista a validar
     * @return true si list es null o isEmpty
     */
    @SuppressWarnings("rawtypes")
	public static boolean isNullOrEmpty( List list ) {
        return list == null || list.isEmpty();
    }

    /**
     * Valida si un mapa es nulo o vacio
     *
     * @param map Mapa a validar
     * @return true si map es null o isEmpty
     */
    @SuppressWarnings("rawtypes")
	public static boolean isNullOrEmpty(Map map) {
        return map == null || map.isEmpty();
    }
    
    /**
     * Valida si un objeto Double es nulo o CERO
     *
     * @param obj Long a validar
     * @return true si es null
     */
    public static boolean isGreaterThanZero( Integer num ) {
        return num > GeneralConstants.ZERO;
    }
    
    /** 
     * Valida el menor que entre bytes.
     */
    
    public static boolean isLessThanInBytes( Long numBytes, int numMB ) {
    	return numBytes / GeneralConstants.MB_IN_KILOBYTES < numMB * GeneralConstants.MB_IN_KILOBYTES;
    }
    
    /**
     * Metodo que valida que el nombre del archivo sea valido.
     * 
     * @param fileName: nombre del archivo a validar.
     * @return true si el string cumple el criterio de la expresion regular, de lo contrario devuelve false.
     */
    public static boolean isValidName(String fileName) {
    	// TODO: Actualizar el regex para aceptar mas de un punto, pero no 2 puntos consecutivos y algunos caraceres especiales. Los que sean validos para fileSystem.
    	// Probar este regex: "[^/?*:;{}\\]+\\.[^/?*:;{}\\]+"
    	return fileName.matches("[\\-\\w+.]+\\.\\w+");
    }
    
    /**
     * Compara dos valores long y regresa true si estos dos valores son numericamente iguales
     * @param l
     * @param l2
     * @return
     */
    public static boolean isEqual(Long l, Long l2) {
    	return l.compareTo(l2) == GeneralConstants.ZERO;
    }
    
    /**
     * Compara dos valores long y regresa true si estos dos valores son numericamente distintos
     * @param l
     * @param l2
     * @return
     */
    public static boolean isDifferent(Long l, Long l2) {
    	return l.compareTo(l2) != GeneralConstants.ZERO;
    }
    
    public static boolean isEqual(String str1, String str2) {
    	return str1.equals(str2);
    }
    
}
