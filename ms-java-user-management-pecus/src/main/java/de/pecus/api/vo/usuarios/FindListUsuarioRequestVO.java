package de.pecus.api.vo.usuarios;

import java.io.Serializable;

public class FindListUsuarioRequestVO implements Serializable {

	/**
	 * Serial version UID de la clase
	 */
	private static final long serialVersionUID = -8441357256099039125L;
	private String email;
	private String telefono;
	
	/**
	 * @return the email
	 */
	public String getEmail() {
		return email;
	}
	/**
	 * @param email the email to set
	 */
	public void setEmail(String email) {
		this.email = email;
	}
	/**
	 * @return the telefono
	 */
	public String getTelefono() {
		return telefono;
	}
	/**
	 * @param telefono the telefono to set
	 */
	public void setTelefono(String telefono) {
		this.telefono = telefono;
	}
}
