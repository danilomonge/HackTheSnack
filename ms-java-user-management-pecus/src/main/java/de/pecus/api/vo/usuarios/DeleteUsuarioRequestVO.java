package de.pecus.api.vo.usuarios;

import java.io.Serializable;

public class DeleteUsuarioRequestVO implements Serializable {
 
	/**
	 * Serial Version UID de la clase
	 */
	private static final long serialVersionUID = 5073307729385941280L;
	
	private Long idUsuario;

	/**
	 * @return the idUsuario
	 */
	public Long getIdUsuario() {
		return idUsuario;
	}

	/**
	 * @param idUsuario the idUsuario to set
	 */
	public void setIdUsuario(Long idUsuario) {
		this.idUsuario = idUsuario;
	}
}
