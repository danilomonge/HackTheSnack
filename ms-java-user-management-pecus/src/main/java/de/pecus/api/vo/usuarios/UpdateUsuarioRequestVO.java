/**
 * 
 */
package de.pecus.api.vo.usuarios;

import java.io.Serializable;

/**
 * @author LuisEnriqueSanchezSa
 *
 */
public class UpdateUsuarioRequestVO implements Serializable {

	/**
	 * Serial version UID de la clase
	 */
	private static final long serialVersionUID = 531925153985191492L;
	
	private Long id;
	private Long idPersona;
	private Long idMedico;
	private Long idPaciente;
    private String email;
    private String telefono;
    private String imagenPerfil;
    private String password;
    private Boolean notificaciones;
    
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
	 * @return the idPersona
	 */
	public Long getIdPersona() {
		return idPersona;
	}
	/**
	 * @param idPersona the idPersona to set
	 */
	public void setIdPersona(Long idPersona) {
		this.idPersona = idPersona;
	}
	/**
	 * @return the idMedico
	 */
	public Long getIdMedico() {
		return idMedico;
	}
	/**
	 * @param idMedico the idMedico to set
	 */
	public void setIdMedico(Long idMedico) {
		this.idMedico = idMedico;
	}
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
}
