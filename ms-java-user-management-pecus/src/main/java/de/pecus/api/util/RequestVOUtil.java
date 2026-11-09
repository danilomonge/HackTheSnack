package de.pecus.api.util;

import java.util.Map;

import de.pecus.api.enums.CommonHeadersEnum;
import de.pecus.api.vo.RequestVO;

/**
 * Utileria para las transformaciones del objeto RequestVO de un tipo
 * parametrizado a otro
 * 
 * @author Juan Carlos Contreras
 */
public class RequestVOUtil {

    private RequestVOUtil() {
    }

    /**
     * Metodo para transformar un requestVO de un tipo a otro.
     * 
     * Este metodo cuida que los parametros generales que viajan dentro del
     * RequestVO, sean transmitidos a otro RequestVO al momento de transformarlo,
     * con la finalidad de que se mantengan los objetos necesarios para el uso del
     * SmartLogger y temas de validacion a traves del token.
     * 
     * Ejemplo de uso; supongamos que desde la operacion: 
     * 
     *     TicketService.asignarTokenUsuario(RequestVO<AsignarTokenUsuarioRequestVO>requestVO)
     *     
     * Requerimos obtener un usuario para validar que al usuario que queremos
     * asignarle el token, cuenta con el rol indicado.
     * 
     * En este escenario tenemos que construir un RequestVO<UsuarioVO> para obtener
     * el usuario y de esta forma poder validar que el usuario cuenta con el rol que
     * se requiere. Para poder propagar los datos que se encuentran dentro del
     * objeto RequestVO<AsignarTokenUsuarioRequestVO> podemos hacerlo como se
     * muestra a continuacion:
     * 
     * ResponseVO<AsignarTokenResponseVO> asignarTokenUsuario(RequestVO<AsignarTokenUsuarioRequestVO> requestVO) {
     *    ResponseVO<AsignarTokenResponseVO> response = new ResponseVO<AsignarTokenResponseVO>();
     *    
     *    // Creamos el objeto del tipo que queremos obtener
     *    UsuarioVO usuarioVO = new UsuarioVO();
     *    usuarioVO.setId(requestVO.getParameters().getIdUsuario());
     *    
     *    // Hacemos la transformacion
     *    Request<UsuarioVO> requestUsuarioVO = RequestVOUtil.setNewRequestVO(requestVO, usuarioVO);
     *    
     *    ...
     *    codigo del servicio
     *    ...
     *    
     *    return response;
     * }
     * 
     * @param <T> Objeto request original
     * @param <K> Objeto request al que queremos transformar
     */
    public static final <T, K> RequestVO<K> setNewRequestVO(RequestVO<T> originalRequestVO, K parameters) {
        RequestVO<K> newRequestVO = new RequestVO<>();
        newRequestVO.setOrderBy(originalRequestVO.getOrderBy());
        newRequestVO.setOrderType(originalRequestVO.getOrderType());
        newRequestVO.setPage(originalRequestVO.getPage());
        newRequestVO.setParameters(parameters);
        newRequestVO.setSize(originalRequestVO.getSize());
        newRequestVO.setSmartLoggerVO(originalRequestVO.getSmartLoggerVO());
        newRequestVO.setToken(originalRequestVO.getToken());
        newRequestVO.setIdioma(originalRequestVO.getIdioma());
        newRequestVO.setLatitude(originalRequestVO.getLatitude());
        newRequestVO.setLongitude(originalRequestVO.getLongitude());
        newRequestVO.setTimeZoneUsuario(originalRequestVO.getTimeZoneUsuario());
        return newRequestVO;
    }
    
    /**
     * Metodo para generar objeto RequestVO y setear encabezados
     * @param <K>
     * @param headers
     * @param parameters
     * @return
     */
	public static final <K> RequestVO<K> setNewRequestVO(Map<String, String> headers, K parameters) {
		RequestVO<K> newRequestVO = new RequestVO<>();
		newRequestVO.setParameters(parameters);
		setCommonHeaders(headers, newRequestVO);
		return newRequestVO;
	}

	/**
	 * Metodo para generar objeto RequestVO, setear encabezados y parametros de paginacion
	 * @param <K>
	 * @param headers
	 * @param page
	 * @param size
	 * @param orderBy
	 * @param orderType
	 * @param parameters
	 * @return
	 */
	public static final <K> RequestVO<K> setNewRequestVO(Map<String, String> headers, Integer page, Integer size,
			String orderBy, String orderType, K parameters) {
		RequestVO<K> newRequestVO = new RequestVO<>();	
		newRequestVO.setOrderBy(orderBy);
		newRequestVO.setOrderType(orderType);
		newRequestVO.setPage(page);
		newRequestVO.setParameters(parameters);
		newRequestVO.setSize(size);
		setCommonHeaders(headers, newRequestVO);
		return newRequestVO;
	}
    
	/**
	 * Metodo para setear encabezados a objeto RequestVO
	 * @param <K>
	 * @param headers
	 * @param newRequestVO
	 */
    private static <K> void setCommonHeaders(Map<String, String> headers, RequestVO<K> newRequestVO) {
    	if(ValidatorUtil.isNullOrEmpty(headers.get(CommonHeadersEnum.AUTHORIZATION.getKey()))) {
    		newRequestVO.setToken(headers.get(CommonHeadersEnum.AUTHORIZATION.getKey().toLowerCase()));
    	}else {
    		newRequestVO.setToken(headers.get(CommonHeadersEnum.AUTHORIZATION.getKey()));
    	}
    	newRequestVO.setIdioma(headers.get(CommonHeadersEnum.LANGUAGE.getKey()));
    	newRequestVO.setLatitude(NumberUtil.stringToDouble(headers.get(CommonHeadersEnum.LATITUDE.getKey())));
    	newRequestVO.setLongitude(NumberUtil.stringToDouble(headers.get(CommonHeadersEnum.LONGITUDE.getKey())));
    	newRequestVO.setTimeZoneUsuario(headers.get(CommonHeadersEnum.TIME_ZONE.getKey()));
    	newRequestVO.setCodigoOperacionCliente(headers.get(CommonHeadersEnum.CODIGO_OPERACION_CLIENTE.getKey()));
    	newRequestVO.setIdClienteInvoke(headers.get(CommonHeadersEnum.ID_CLIENTE_INVOKE.getKey()));
    	newRequestVO.setRequestDate(
    			DateTimeUtil.stringToDateWithTimeZone(headers.get(CommonHeadersEnum.REQUEST_DATE.getKey()),
    					headers.get(CommonHeadersEnum.TIME_ZONE.getKey())));
    	newRequestVO.setMacAddress(headers.get(CommonHeadersEnum.MAC_ADDRESS.getKey()));
    }
}