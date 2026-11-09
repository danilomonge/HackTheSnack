package de.pecus.api.util;

import java.text.MessageFormat;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.lang.RandomStringUtils;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import de.pecus.api.constant.GeneralConstants;

/**
 * Clase de utileria para conversion de cadenas
 * 
 */
public final class StringUtil {

	private static final Logger LOGGER = LoggerFactory.getLogger(StringUtil.class);

	/**
	 * Constructor privado para evitar instanciacion de clase
	 */
	private StringUtil() {

	}

	/**
	 * Valida si un objeto string es nulo o vacio
	 *
	 * @param str String a validar
	 * @return true si str es null o isEmpty
	 */
	public static boolean isNullOrEmpty(String str) {
		return str == null || str.isEmpty();
	}

	/**
	 * Valida si un objeto string contiene la cadena null.
	 *
	 * @param str String a validar
	 * @return true si str es null o isEmpty
	 */
	public static boolean isNullString(String str) {
		return str == null || str.isEmpty() || GeneralConstants.NULL.equals(str);
	}

	public static String padStart(String string, int minLength, char padChar) {
		if (string == null || string.length() >= minLength) {
			return string;
		}
		StringBuilder sb = new StringBuilder(minLength);
		for (int i = string.length(); i < minLength; i++) {
			sb.append(padChar);
		}
		sb.append(string);
		return sb.toString();
	}

	public static String getEmptyIfNull(String value) {
		if (value == null) {
			return GeneralConstants.EMPTY_STRING;
		}
		return value;
	}

	public static String trim(String value) {
		if (value == null) {
			return value;
		}
		return value.trim();
	}

	public static String getSplitElement(String s, String regex, int n) {
		String element = null;
		if (s != null) {
			String[] split = s.split(regex);
			if (split != null && split.length >= n) {
				element = split[n];
			}
		}
		return element;
	}

	/**
	 * Metodo que construye una cadena mutable en base a los argumentos
	 * proporcionados.
	 * 
	 * @param args Argumentos para construir la cadena mutable.
	 * @return {@link StringBuilder} con la cadena mutable en base a los argumentos
	 *         proporcionados.
	 * @author afuentes
	 */
	public static StringBuilder buildMutableString(Object... args) {
		StringBuilder builder = new StringBuilder();
		for (Object object : args) {
			builder.append(object);
		}
		return builder;
	}

	/**
	 * Metodo que construye una cadena usando una cadena mutable en base a los
	 * argumentos proporcionados.
	 * 
	 * @param args Argumentos para construir la cadena mutable.
	 * @return {@link String} con la cadena no mutable en base a los argumentos
	 *         proporcionados.
	 * @author afuentes
	 */
	public static String buildStringUsingMutable(Object... args) {
		return buildMutableString(args).toString();
	}

	/**
	 * Trunca la cadena al tamanio especificado, eliminando espacios al inicio y fin
	 * 
	 * @param str  Cadena a truncar
	 * @param size Tamanio maximo a truncar
	 * @return Cadena truncada o null si str es null
	 */
	public static String substring(String str, int size) {
		String formatStr = null;
		if (str != null) {
			formatStr = str.trim();
			formatStr = formatStr.substring(GeneralConstants.ZERO, Math.min(size, formatStr.length()));
			formatStr = formatStr.trim();
		}
		return formatStr;
	}

	/**
	 * Convierte la cadena a mayusculas validando que no sea null
	 * 
	 * @param str Cadena a convertir
	 * @return Cadena convertida o null si str es null
	 */
	public static String toUpperCase(String str) {
		String formatStr = null;
		if (str != null) {
			formatStr = str.toUpperCase();
		}
		return formatStr;
	}

	/**
     * Valida si el formato de una cadena satisface el formato de un correo electronico
     * @param str Cadena a validar
     * @return boolean que indica si la caden es valida
     */
    public static boolean isValidEmail(String email)
    {
    	if(ValidatorUtil.isNullOrEmpty(email)) {
    		return false;
    	}
    	try{
    		Pattern pattern = Pattern
                .compile("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");
    	Matcher matcher = pattern.matcher(email);
    	return matcher.find();
    	} catch (Exception e) {
    		return false;
    	}
	}

	/**
	 * Reemplaza todas las ocurrencias.
	 * 
	 * @param sb      cadena origen
	 * @param find    cadena a remplazarse
	 * @param replace nueva valor de la cadena
	 * @return cadena con los reemplazos
	 */
	public static StringBuilder replaceAll(StringBuilder sb, String find, String replace) {
		StringBuilder replaceBuilder = null;
		try {
			if (!ValidatorUtil.isNullOrEmpty(replace)) {
				replaceBuilder = new StringBuilder(
						Pattern.compile(find).matcher(sb).replaceAll(Matcher.quoteReplacement(replace)));
			} else {
				replaceBuilder = sb;
			}
		} catch (Exception e) {
			LOGGER.error(MessageFormat.format(
					"No se pudo reemplazar en la cadena [{0}], el placeholder [{1}], con el valor [{2}]", sb.toString(),
					find, replace), e);
			throw e;
		}
		return replaceBuilder;
	}

	public static String generateRandomPassword() { 
		return RandomStringUtils.randomNumeric(5);
	}
	
	public static String generateRandomPassword(int size) { 
		return RandomStringUtils.randomNumeric(size);
	}


	/**
	 * Valida si el formato de una cadena satisface el formato de una URL
	 * 
	 * @param str Cadena a validar
	 * @return boolean que indica si la caden es valida
	 */
	public static boolean isValidURL(String url) {
		Pattern pattern = Pattern.compile("^(https?://|www.)[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]");
		Matcher matcher = pattern.matcher(url);
		return matcher.find();
	}

	public static String obtenerNombreCompleto(String primerApellido, String segundoApellido, String... nombres) {

		try {
			StringBuilder nombreCompleto = new StringBuilder("");

			if (!ValidatorUtil.isNull(nombres)) {
				for (String nom : nombres) {
					nombreCompleto.append(nom != null ? nom : "").append(GeneralConstants.SPACE_STRING);
				}
			}
			if (!ValidatorUtil.isNullOrEmpty(primerApellido)) {
				nombreCompleto.append(primerApellido);
			}
			if (!ValidatorUtil.isNullOrEmpty(segundoApellido)) {
				nombreCompleto.append(GeneralConstants.SPACE_STRING).append(segundoApellido);
			}
			return nombreCompleto.toString();
		} catch (Exception ex) {
			return null;
		}
	}

	/**
	 * Metodo que agrega un parametro a una cadena, validando que no sea null
	 * @param buffer StringBufer al que se agrega el parametro
	 * @param param Objeto con el parametro
	 * @param format Formato para String.format que se utiliza para agregar cadenas fijas
	 * antes o despues del objeto
	 */
	public static void appendIfNotNull(StringBuffer buffer, Object param, String format) {
		if(!ValidatorUtil.isNull(param)) {
			buffer.append(String.format(format, param));
		}
	}
	
	/**
	 * Metodo que convierte los caracteres mayusculas a minusculas y remueve acentos
	 * @param input String de entrada
	 * @return string en minusculas y sin acentos
	 */
	public static String toLowerStripAccents(String input) {
		return (input != null) ? StringUtils.stripAccents(input).toLowerCase() : null;
	}

}
