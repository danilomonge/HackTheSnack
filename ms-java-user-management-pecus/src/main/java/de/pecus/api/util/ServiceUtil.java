package de.pecus.api.util;

import java.lang.reflect.Field;
import java.text.ParseException;
import java.util.Calendar;
import java.util.Date;
import java.util.Map;
import java.util.TimeZone;

import org.bouncycastle.util.encoders.Base64;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.nimbusds.jose.JOSEException;
import com.nimbusds.jose.JWSAlgorithm;
import com.nimbusds.jose.JWSHeader;
import com.nimbusds.jose.JWSObject;
import com.nimbusds.jose.KeyLengthException;
import com.nimbusds.jose.Payload;
import com.nimbusds.jose.crypto.MACSigner;

import de.pecus.api.constant.GeneralConstants;
import de.pecus.api.entities.AuditBase;
import de.pecus.api.entities.I18nBase;
import de.pecus.api.entities.IdiomaDO;
import de.pecus.api.vo.RequestVO;
import net.minidev.json.JSONObject;

/**
 * Clase de utileria para conversion de cadenas
 * 
 */
public final class ServiceUtil {

	/**
	 * Logger
	 */
	private static final Logger LOGGER = LoggerFactory.getLogger(ServiceUtil.class);

	/**
	 * Constructor privado para evitar instanciacion de clase
	 */
	private ServiceUtil() {

	}

	public static void setAuditFields(AuditBase<?> entity, String token) {
		Long userId;
		if(ValidatorUtil.isNullOrEmpty(token)) {
			userId = 1L;
		}else {
			userId = ServiceUtil.extractLongFieldFromToken(token, GeneralConstants.USER_ID);
		}
		
		Date date = new Date();
		if (ValidatorUtil.isNull(entity.getCreationDate())) {
			entity.setCreationDate(date);
			entity.setCreatorUsername(userId);
		}
		entity.setLastModifiedDate(date);
		entity.setLastModifiedUsername(userId);
		entity.setActive(Boolean.TRUE);
		
	}

	public static void setDisabledEntity(AuditBase<?> entity, String token) {
		setAuditFields(entity, token);
		entity.setActive(Boolean.FALSE);
	}
	
	/**
	 * Setea el idioma en la entidad
	 * 
	 * @param entity a setear
	 * @param token 
	 */
	@SuppressWarnings("unchecked")
	public static void setLenguage(I18nBase<?> entity, String token) {

		AuditBase<?> auditBase = (AuditBase<?>) entity;
		// Setea campos de auditoria
		setAuditFields(auditBase, token);

		Map<String, Object> tokenMap = ServiceUtil.extractFieldObjectValueFromToken(token, GeneralConstants.IDIOMA_VO);
		// se transforma el idiomaDO
		IdiomaDO idiomaDO = transformIdiomaDO(tokenMap);

		entity.setIdioma(idiomaDO);
	}

	/**
	 * Obtiene un IdiomaDO a partir de un tokenMap
	 * 
	 * @param tokenMap a transformar
	 * @return Objeto de transporte DO para retorno de resultados
	 */
	public static IdiomaDO transformIdiomaDO(Map<String, Object> tokenMap) {

		IdiomaDO idiomaDO = new IdiomaDO();

		if (tokenMap != null) {
			Long id = (Long) tokenMap.get("id");
			String idNombre = (String) tokenMap.get("idNombre");
			String descripcion = (String) tokenMap.get("descripcion");

			idiomaDO.setId(id);
			idiomaDO.setIdNombre(idNombre);
			idiomaDO.setDescripcion(descripcion);
		}

		return idiomaDO;
	}
	
	public static Long getUser(String token) {
		return ServiceUtil.extractLongFieldFromToken(token, GeneralConstants.USER_ID);
	}

	/**
	 * Obtiene el limite inicial de la paginacion a partir del numero de pagina
	 * 
	 * @param request Objeto con parametros de paginacion
	 * 
	 * @return Limite inicial: (page - 1) * size
	 */
	public static <T> Integer getPaginationStart(RequestVO<T> request) {
		return (request.getPage() - 1) * request.getSize();
	}
	
	/**
	 * Obtiene el limite inicial de la paginacion a partir del numero de pagina
	 * 
	 * @param request Objeto con parametros de paginacion
	 * 
	 * @return Limite inicial: (page - 1) * size
	 */
	public static <T> Integer getRealPage(RequestVO<T> request) {
		return request.getPage() - 1;
	}

	/**
	 * Obtiene la fecha de sistema
	 * 
	 * @param timezone (Opcional) El timezone que se usara para obtener la fecha de sistema (ej. "PST","America/Los_Angeles","GMT-8:00")
	 * 
	 * 
	 * @return Instancia de fecha. Si no se manda la zona horaria o es inentendible se usa GTM
	 */
	public static Date getCurrentDate(String timezone) {
		if(StringUtil.isNullOrEmpty(timezone)){
			return Calendar.getInstance().getTime();
		}else{
			return Calendar.getInstance(TimeZone.getTimeZone(timezone)).getTime();
		}
	}
	/**
	 * Obtiene la fecha de sistema
	 * 
	 * @param timezone (Opcional) El timezone que se usara para obtener la fecha de sistema (ej. "PST","America/Los_Angeles","GMT-8:00")
	 * 
	 * 
	 * @return Instancia de fecha. Si no se manda la zona horaria o es inentendible se usa GTM
	 */
	public static Date getCurrentDate() {
		return Calendar.getInstance().getTime();
	}



	/**
	 * Obtiene la fecha de sistema para timezone de México
	 * 
	 * @return Instancia de fecha 
	 */
	public static Date getCurrentDateMexicoCity() {
		return Calendar.getInstance(TimeZone.getTimeZone(GeneralConstants.MEXICO_CITY_TIMEZONE)).getTime();
	}

	/**
	 * Obtiene un parametro del token
	 * 
	 * @param token     Token de sesion
	 * @param fieldName Nombre del campo requerido
	 * 
	 * @return Cadena con el valor del atributo obtenido
	 */
	public static String extractFieldValueFromToken(String token, String fieldName) {
		String fieldValue = null;
		JWSObject jwsObject;
		if (!StringUtil.isNullOrEmpty(token)) {
			try {
				 if (token.startsWith("Bearer ")) {
				     token = token.substring(7, token.length());
				    }
				jwsObject = JWSObject.parse(token);
				JSONObject jsonObject = jwsObject.getPayload().toJSONObject();
				jsonObject = (JSONObject) jsonObject.get(GeneralConstants.TOKEN_DATA);
				if(!ValidatorUtil.isNull(jsonObject)) {
					Object fieldValueObj = jsonObject.get(fieldName);
					if (fieldValueObj != null) {
						fieldValue = fieldValueObj.toString();
					}
				}
			} catch (ParseException e) {
				LOGGER.error("ServiceUtil extractFieldValueFromToken ParseException", e.getMessage());
			}
		}
		return fieldValue;
	}

	/**
	 * Obtiene un parametro del token
	 * 
	 * @param token     Token de sesion
	 * @param fieldName Nombre del campo requerido
	 * 
	 * @return Objeto con el valor del atributo obtenido
	 */
	@SuppressWarnings("rawtypes")
	public static Map extractFieldObjectValueFromToken(String token, String fieldName) {
		Map fieldValueObj = null;
		JWSObject jwsObject;
		if (!StringUtil.isNullOrEmpty(token)) {
			try {
				if (token.startsWith("Bearer ")) {
				     token = token.substring(7, token.length());
				    }
				jwsObject = JWSObject.parse(token);
				JSONObject jsonObject = jwsObject.getPayload().toJSONObject();
				jsonObject = (JSONObject) jsonObject.get(GeneralConstants.TOKEN_DATA);

				fieldValueObj = (Map) jsonObject.get(fieldName);
			} catch (ParseException e) {
				LOGGER.error("ServiceUtil extractFielObjectdValueFromToken ParseException", e);
			}
		}
		return fieldValueObj;
	}
	
	/**
	 * Obtiene un parametro del token en formato long
	 * 
	 * @param token     Token de sesion
	 * @param fieldName Nombre del campo requerido
	 * 
	 * @return Cadena con el valor del atributo obtenido
	 */
	private static Long extractLongFieldFromToken(String token, String fieldName) {
		String fieldValue = extractFieldValueFromToken(token, fieldName);
		Long longValue = null;
		if (!ValidatorUtil.isNull(fieldValue)) {
			longValue = Long.parseLong(fieldValue);
		}
		return longValue;
	}

	/**
	 * Obtiene un parametro del token en formato boolean
	 * 
	 * @param token     Token de sesion
	 * @param fieldName Nombre del campo requerido
	 * 
	 * @return Cadena con el valor del atributo obtenido
	 */
	public static Boolean extractBooleanFieldFromToken(String token, String fieldName) {
		String fieldValue = extractFieldValueFromToken(token, fieldName);
		Boolean booleanValue = null;
		if (!ValidatorUtil.isNull(fieldValue)) {
			booleanValue = Boolean.parseBoolean(fieldValue);
		}
		return booleanValue;
	}
	
	
	
	
	/**
	 * Genera un token para ResponseVO
	 * @param <T>
	 * 
	 * @param usuario Usuario autenticado
	 * 
	 * @return Cadena con token generado
	 */
	public static <T> String create(T data) {

		JSONObject json = new JSONObject();

		json.put(GeneralConstants.TOKEN_DATA, data);

		JWSObject jwsObject = new JWSObject(new JWSHeader(JWSAlgorithm.HS256), new Payload(json));

		try {
			jwsObject.sign(new MACSigner(getSigningKey()));
		} catch (KeyLengthException e) {
			LOGGER.error("TokenService KeyLengthException ", e);

		} catch (JOSEException e) {
			LOGGER.error("TokenService JOSEException ", e);
		}

		return jwsObject.serialize();
	}
	
	
	/**
	 * Obtiene el shared key
	 * 
	 * @return Key leido
	 */
	private static byte[] getSigningKey() {

		byte[] key = null;

		key = Base64.decode(findKey());

		return key;

	}

	private static String findKey() {

		// obtener de tabla de parametros

		return GeneralConstants.TOKEN_KEY;

	}
	
	/**
	 * Genera un token para ResponseVO
	 * @param <T>
	 * @param <T>
	 * 
	 * @param usuario Usuario autenticado
	 * 
	 * @return Cadena con token generado
	 */
	@SuppressWarnings({ "unchecked", "unused" })
    public static  <T> T convertJWTObject(T clazz, String token) {
		
		T newInstance = null;
		
		if (!StringUtil.isNullOrEmpty(token)) {
			
			 ObjectMapper mapper = new ObjectMapper();
			 
			try {
				
				JWSObject jwsObject;
				
				jwsObject = JWSObject.parse(token);
				JSONObject jsonObject = jwsObject.getPayload().toJSONObject();
				jsonObject = (JSONObject) jsonObject.get(GeneralConstants.TOKEN_DATA);
				
				 newInstance = (T) clazz.getClass().newInstance();

				for  (Field field: clazz.getClass().getDeclaredFields() ) {
					field.setAccessible(true);
					field.set(newInstance, jsonObject.get(field.getName()));
					field.setAccessible(false);
				}
				
				System.out.println(newInstance);
			
			} catch (Exception e) {
				LOGGER.error("ServiceUtil extractFielObjectdValueFromToken ParseException", e);
			}
		}
		return newInstance;
		
		
	}
	

	
	
	

}
