package de.pecus.api.vo.usuarios;

import java.io.Serializable;
import java.util.Date;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;

import de.pecus.api.constant.GeneralConstants;

@JsonInclude(Include.NON_NULL)
public class FindListUsuarioResponseVO implements Serializable {

    /**
	 * Serial version UID de la clase
	 */
	private static final long serialVersionUID = -4647630949071070212L;
	private Long id;
    private Boolean notificationsEnabled;
    private String userIdEmail;
    private String userIdMobileDevice;
    private String userIdMobileNumber;
    private String imagenPerfil;
    private String ladaPais;
    @JsonFormat(pattern=GeneralConstants.DATE_TIME_FORMAT_YYYY_MM_DD, timezone = "America/Mexico_City")
    private Date terminosAceptados;
    private Long idPersona;
    private Long idPaciente;
    private Long idMedico;
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
	 * @return the notificationsEnabled
	 */
	public Boolean getNotificationsEnabled() {
		return notificationsEnabled;
	}
	/**
	 * @param notificationsEnabled the notificationsEnabled to set
	 */
	public void setNotificationsEnabled(Boolean notificationsEnabled) {
		this.notificationsEnabled = notificationsEnabled;
	}
	/**
	 * @return the userIdEmail
	 */
	public String getUserIdEmail() {
		return userIdEmail;
	}
	/**
	 * @param userIdEmail the userIdEmail to set
	 */
	public void setUserIdEmail(String userIdEmail) {
		this.userIdEmail = userIdEmail;
	}
	/**
	 * @return the userIdMobileDevice
	 */
	public String getUserIdMobileDevice() {
		return userIdMobileDevice;
	}
	/**
	 * @param userIdMobileDevice the userIdMobileDevice to set
	 */
	public void setUserIdMobileDevice(String userIdMobileDevice) {
		this.userIdMobileDevice = userIdMobileDevice;
	}
	/**
	 * @return the userIdMobileNumber
	 */
	public String getUserIdMobileNumber() {
		return userIdMobileNumber;
	}
	/**
	 * @param userIdMobileNumber the userIdMobileNumber to set
	 */
	public void setUserIdMobileNumber(String userIdMobileNumber) {
		this.userIdMobileNumber = userIdMobileNumber;
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
	 * @return the ladaPais
	 */
	public String getLadaPais() {
		return ladaPais;
	}
	/**
	 * @param ladaPais the ladaPais to set
	 */
	public void setLadaPais(String ladaPais) {
		this.ladaPais = ladaPais;
	}
	/**
	 * @return the terminosAceptados
	 */
	public Date getTerminosAceptados() {
		return terminosAceptados;
	}
	/**
	 * @param terminosAceptados the terminosAceptados to set
	 */
	public void setTerminosAceptados(Date terminosAceptados) {
		this.terminosAceptados = terminosAceptados;
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
}
