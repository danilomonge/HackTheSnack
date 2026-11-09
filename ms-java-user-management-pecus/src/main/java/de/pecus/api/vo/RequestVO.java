package de.pecus.api.vo;

import java.io.Serializable;
import java.util.Date;

import com.fasterxml.jackson.annotation.JsonIgnore;

/**
 * Clase con datos base para respuesta de servicios
 * 
 *
 * @param <T> Clase con datos especificos de la resuesta
 */
public class RequestVO<T> implements Serializable{

	/** Indica la pagina a consultar */
    private Integer page;

    /** Indica el tamano de la pagina */
    private Integer size;

    @JsonIgnore
    /** Token de sesion */
    private String token;

    /** MAC Address del dispositivo que envia la peticion */
    private String macAddress;

    /** Objeto con los parametros de la consulta */
    private T parameters;
    
    /** Fecha enviada por el cliente para indicar el momento de la peticion */
    private Date requestDate;

    @JsonIgnore
    /** Se asigna el SmartLogger para la bitácora **/
    private SmartLoggerVO smartLoggerVO;

    /** Oredenar por nombre de columna **/
    private String orderBy;

    /** Tipo de ordenamiento (ASC,DESC) **/
    private String orderType;

    /** Latitud del dispositivo que realiza la peticion */
    private Double latitude;

    /** Longitud del dispositivo que realiza la peticion */
    private Double longitude;

    /** Idioma del la peticion */
    private String idioma;

    /**
     * TimeZone con el que se desea realizar la busqueda de acuerdo al timezone
     * actual del usuario
     */
    private String timeZoneUsuario;
    
    /**
     * Número logico que se la da al cliente que invoca al servicio para ser identifcado
     * en la bitacora de auditorias por las areas de operaciones
     * 
     */
    private String idClienteInvoke;
    
    /**
     * Identificador proporcionado por el consumidor del servicio que permite correlacionar
     * su proceso con los servicios invocados
     * 
     * por ejemplo: numero de poliza, numero de estudio que le permita al consumidor identificar
     * su propia operacion.
     * 
     */
    private String codigoOperacionCliente;
   

    /**
     * Constructor sin argumentos
     */
    public RequestVO() {

    }

    /**
     * Constructor con parametautorizacionros por defecto
     * 
     * @param page  Numero de pagina
     * @param size  Tamano de pagina
     * @param token Token de sesion
     */
    public RequestVO(Integer page, Integer size, String token, T parameters, String orderBy, String orderType,
            String idioma) {
        this.page = page;
        this.size = size;
        this.token = token;
        this.parameters = parameters;
        this.orderBy = orderBy;
        this.orderType = orderType;
        this.idioma = idioma;
    }

    /**
     * Constructor con token y parametros
     * 
     * @param token      Tojen de sesion
     * @param parameters
     */
    public RequestVO(String token, T parameters) {
        this.token = token;
        this.parameters = parameters;
    }

    /**
     * @return the page
     */
    public Integer getPage() {
        return page;
    }

    /**
     * @param page the page to set
     */
    public void setPage(Integer page) {
        this.page = page;
    }

    /**
     * @return the size
     */
    public Integer getSize() {
        return size;
    }

    /**
     * @param size the size to set
     */
    public void setSize(Integer size) {
        this.size = size;
    }

    /**
     * @return the token
     */
    public String getToken() {
        return token;
    }

    /**
     * @param token the token to set
     */
    public void setToken(String token) {
        this.token = token;
    }

    /** @return the mac address */
    public String getMacAddress() {
        return macAddress;
    }

    /** @param mac address del dispositivo */
    public void setMacAddress(String macAddress) {
        this.macAddress = macAddress;
    }

    /**
     * @return the parameters
     */
    public T getParameters() {
        return parameters;
    }

    /**
     * @param parameters the parameters to set
     */
    public void setParameters(T parameters) {
        this.parameters = parameters;
    }

    /**
     * @return the request date
     */
    public Date getRequestDate() {
        return requestDate;
    }

    /**
     * @param requestDate
     */
    public void setRequestDate(Date requestDate) {
        this.requestDate = requestDate;
    }

    public SmartLoggerVO getSmartLoggerVO() {
        return smartLoggerVO;
    }

    public void setSmartLoggerVO(SmartLoggerVO smartLoggerVO) {
        this.smartLoggerVO = smartLoggerVO;
    }

    /**
     * @return the orderBy
     */
    public String getOrderBy() {
        return orderBy;
    }

    /**
     * @param orderBy the orderBy to set
     */
    public void setOrderBy(String orderBy) {
        this.orderBy = orderBy;
    }

    /**
     * @return the orderType
     */
    public String getOrderType() {
        return orderType;
    }

    /**
     * @param orderType the orderType to set
     */
    public void setOrderType(String orderType) {
        this.orderType = orderType;
    }

    /**
     * @return the latitude of the device
     */
    public Double getLatitude() {
        return latitude;
    }

    /**
     * @param latitude of the device
     */
    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    /**
     * @return the longitude of the device
     */
    public Double getLongitude() {
        return longitude;
    }

    /**
     * @param longitude of the device
     */
    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    public String getIdioma() {
        return idioma;
    }

    public void setIdioma(String idioma) {
        this.idioma = idioma;
    }

    public String getTimeZoneUsuario() {
        return timeZoneUsuario;
    }

    public void setTimeZoneUsuario(String timeZoneUsuario) {
        this.timeZoneUsuario = timeZoneUsuario;
    }

	public String getIdClienteInvoke() {
		return idClienteInvoke;
	}

	public void setIdClienteInvoke(String idClienteInvoke) {
		this.idClienteInvoke = idClienteInvoke;
	}

	public String getCodigoOperacionCliente() {
		return codigoOperacionCliente;
	}

	public void setCodigoOperacionCliente(String codigoOperacionCliente) {
		this.codigoOperacionCliente = codigoOperacionCliente;
	}

	@Override
	public String toString() {
		return "RequestVO [page=" + page + ", size=" + size + ", token=" + token + ", parameters=" + parameters
				+ ", requestDate=" + requestDate + ", timeZoneUsuario=" + timeZoneUsuario + "]";
	}
    
    /**
	 * 
	 */
	private static final long serialVersionUID = -167913227631494860L;
}
