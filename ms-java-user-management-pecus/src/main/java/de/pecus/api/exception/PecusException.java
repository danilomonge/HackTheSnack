package de.pecus.api.exception;

import java.util.Arrays;
import java.util.List;

import de.pecus.api.error.BusinessError;
import de.pecus.api.error.BusinessErrorUtil;
import de.pecus.api.vo.ResponseErrorVO;

/**
 * Excepcion particular para manejo de errores
 * 
 * @author Luis Enrique Sanchez Santiago
 */
public class PecusException extends GeneralException {

    private static final long serialVersionUID = 3108641492974585380L;

    private List<ResponseErrorVO> responseErrorList;

    /**
     * Constructor con errores de negocio que debe ser invocado cuando se necesite
     * cortar el flujo de una serie de operaciones hacia la base de datos de una
     * sola operacion.
     * 
     * El caso mas comun es cuando se validan los campos de entrada
     * 
     * @param businessError businessErrror
     */
    public PecusException(List<ResponseErrorVO> responseErrorList) {
        super(responseErrorList);
        this.responseErrorList = responseErrorList;
    }

    /**
     * Constructor con lista de errores de negocio
     * 
     * @param businessError businessErrror
     * @param cause         Causa
     * @param params        Parametros
     */
    public PecusException(BusinessError businessError, Throwable cause, Object... params) {
        super(businessError, cause, params);
    }

    /**
     * Constructor con mensaje
     * 
     * @param message Mensaje
     * @param cause   Causa
     * @param params  Parametros de causa
     */
    public PecusException(String message, Throwable cause, Object... params) {
        super(message, cause, params);
    }

    /**
     * Constructor por nombre de error e idioma
     * @param businessErrorName
     * @param idioma
     */
    public PecusException(String businessErrorName, String idioma) {
    	BusinessError error = BusinessErrorUtil.getBusinessError(businessErrorName, idioma);
        this.responseErrorList = Arrays.asList(new ResponseErrorVO(error.getCode(), error.getKey(), error.getDescription(), null));
    }
    
    public List<ResponseErrorVO> getResponseErrorList() {
        return responseErrorList;
    }

}
