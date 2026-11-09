package de.pecus.api.vo.usuarios;

import java.io.Serializable;

public class FindListUsuarioRequestV2VO implements Serializable {

	/**
	 * Serial version UID de la clase
	 */
	private static final long serialVersionUID = -8441357256099039125L;

	private Long idPaciente;

	/**
	 * @return the idPaciente
	 */
	public Long getIdPaciente() {
		return idPaciente;
	}
	/**
	 * @param idPaciente the idPaciente to set
	 */
	public void setIdPaciente(Long idPaciente) {
		this.idPaciente = idPaciente;
	}
}
