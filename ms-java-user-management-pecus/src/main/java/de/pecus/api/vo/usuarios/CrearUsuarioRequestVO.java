package de.pecus.api.vo.usuarios;

import java.io.Serializable;

public class CrearUsuarioRequestVO implements Serializable {

	/**
	 * Serial Version UID de la clase
	 */
	private static final long serialVersionUID = 7636032653899524207L;

	private Long id;
    private String email;
    private String telefono;
    private String imagenPerfil;
    private String password;
    private Boolean notificaciones;
    private Boolean aceptaTerminos;
    
	/**
	 * @return the id
	 */
	public Long getId() {
		return id;
	}
	/**
	 * @param id the id to set
	 */
	public void setId(Long id) {
		this.id = id;
	}
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
	/**
	 * @return the imagenPerfil
	 */
	public String getImagenPerfil() {
		return imagenPerfil;
	}
	/**
	 * @param imagenPerfil the imagenPerfil to set
	 */
	public void setImagenPerfil(String imagenPerfil) {
		this.imagenPerfil = imagenPerfil;
	}
	/**
	 * @return the password
	 */
	public String getPassword() {
		return password;
	}
	/**
	 * @param password the password to set
	 */
	public void setPassword(String password) {
		this.password = password;
	}
	/**
	 * @return the notificaciones
	 */
	public Boolean getNotificaciones() {
		return notificaciones;
	}
	/**
	 * @param notificaciones the notificaciones to set
	 */
	public void setNotificaciones(Boolean notificaciones) {
		this.notificaciones = notificaciones;
	}
	/**
	 * @return the aceptaTerminos
	 */
	public Boolean getAceptaTerminos() {
		return aceptaTerminos;
	}
	/**
	 * @param aceptaTerminos the aceptaTerminos to set
	 */
	public void setAceptaTerminos(Boolean aceptaTerminos) {
		this.aceptaTerminos = aceptaTerminos;
	}
}
