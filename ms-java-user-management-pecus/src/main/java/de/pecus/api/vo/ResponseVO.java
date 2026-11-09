package de.pecus.api.vo;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;

/**
 * Clase con datos base para respuesta de servicios
 * 
 * @author Luis Enrique Sanchez Santiago
 *
 * @param <T> Clase con datos especificos de la respuesta
 */
@JsonInclude(Include.NON_NULL)
public class ResponseVO<T> implements Serializable {

	

	/** Indica si la peticion fue exitosa o hubo un error */
	private boolean success;

	/** Lista de errores */
	private List<ResponseErrorVO> errors;

	/** Objeto con datos especificos de la resuesta */
	private T data;
	
	/** Indica el numero de resultados */
	private Long totalRows;
	
	/** Para mobile, se devuelven los tokens automaticamente */
	private String newToken;

	/**
	 * @return success=true if everything is ok
	 */
	public boolean getSuccess() {
		return success;
	}

	/**
	 * @param success of the request
	 */
	public void setSuccess(boolean success) {
		this.success = success;
	}

	/**
	 * @return errors list of type ResponseErrorVO
	 */
	public List<ResponseErrorVO> getErrors() {

		if (errors == null) {
			errors = new ArrayList<>();
		}

		return errors;
	}

	/**
	 * @param errors list of type <code>ResponseErrorVO</code>
	 */
	public void setErrors(List<ResponseErrorVO> errors) {
		this.errors = errors;
	}

	/**
	 * @return the data
	 */
	public T getData() {
		return data;
	}

	/**
	 * @param data the data to set
	 */
	public void setData(T data) {
		this.data = data;
	}
	
	/**
	 * @return newToken if it is generated when a mobile client sends an expired token
	 */
	public String getNewToken() {
        return newToken;
    }

	/**
	 * @param newToken dynamically created when a mobile client sends an expired token
	 */
    public void setNewToken(String newToken) {
        this.newToken = newToken;
    }

    /**
     * @return totalRows count of the complete result set of a search without pagination
     */
    public Long getTotalRows() {
		return totalRows;
	}

    /**
     * @param totalRows assigns the total number of search rows without pagination
     */
	public void setTotalRows(Long totalRows) {
		this.totalRows = totalRows;
	}
	
	@Override
    public String toString() {
        return "ResponseVO [success=" + success + ", errors=" + errors + ", data=" + data + "]";
    }
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 8518849504236828594L;
}