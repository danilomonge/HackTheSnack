package de.pecus.api.vo.usuarios;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
@JsonInclude(Include.NON_NULL)
public class CreateUsuarioRequestVO {

    
	/**
     * Identificador
     */
	private Long id;
	
	/**
     * Identificador
     */
	private String imagenPerfil;
	private String userIdEmail;
	
	private String userIdMobileNumber;
	
	private String userIdMobileDevice;
	
	private Boolean notificationsEnabled;
	
	private String password;

    private Integer passwordStatus;
    
    private String relationship;
    
    private String resetPasswordLink;

//	private PersonaVO personaVO;
	
	private String nombreEmpresa;
	
	private Long tipoEmpresaId;
	
	private Long tipoPersonaId;
	
	private String nombrePersona;
	
	private String apellidoPatPersona;
	
	private String apellidoMatPersona;
	
	
	private Boolean isApplicationUser;
	
	
	public CreateUsuarioRequestVO(){
		// Constructor por defecto
	}

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

	public String getUserIdMobileNumber() {
		return userIdMobileNumber;
	}

	public void setUserIdMobileNumber(String userIdMobileNumber) {
		this.userIdMobileNumber = userIdMobileNumber;
	}

	public String getUserIdMobileDevice() {
		return userIdMobileDevice;
	}

	public void setUserIdMobileDevice(String userIdMobileDevice) {
		this.userIdMobileDevice = userIdMobileDevice;
	}

	public Boolean getNotificationsEnabled() {
		return notificationsEnabled;
	}

	public void setNotificationsEnabled(Boolean notificationsEnabled) {
		this.notificationsEnabled = notificationsEnabled;
	}
	
	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}

//	public PersonaVO getPersonaVO() {
//		return personaVO;
//	}
//
//	public void setPersonaVO(PersonaVO personaVO) {
//		this.personaVO = personaVO;
//	}

	public String getNombreEmpresa() {
		return nombreEmpresa;
	}

	public void setNombreEmpresa(String nombreEmpresa) {
		this.nombreEmpresa = nombreEmpresa;
	}

	public Long getTipoEmpresaId() {
		return tipoEmpresaId;
	}

	public void setTipoEmpresaId(Long tipoEmpresaId) {
		this.tipoEmpresaId = tipoEmpresaId;
	}

	public Long getTipoPersonaId() {
		return tipoPersonaId;
	}

	public void setTipoPersonaId(Long tipoPersonaId) {
		this.tipoPersonaId = tipoPersonaId;
	}

	public String getNombrePersona() {
		return nombrePersona;
	}

	public void setNombrePersona(String nombrePersona) {
		this.nombrePersona = nombrePersona;
	}

	public String getApellidoPatPersona() {
		return apellidoPatPersona;
	}

	public void setApellidoPatPersona(String primerApellidoPersona) {
		this.apellidoPatPersona = primerApellidoPersona;
	}

	public String getApellidoMatPersona() {
		return apellidoMatPersona;
	}

	public void setApellidoMatPersona(String segundoApellidoPersona) {
		this.apellidoMatPersona = segundoApellidoPersona;
	}

	public String getImagenPerfil() {
		return imagenPerfil;
	}

	public void setImagenPerfil(String imagenPerfil) {
		this.imagenPerfil = imagenPerfil;
	}

	public Integer getPasswordStatus() {
		return passwordStatus;
	}

	public void setPasswordStatus(Integer passwordStatus) {
		this.passwordStatus = passwordStatus;
	}

	public String getRelationship() {
		return relationship;
	}

	public void setRelationship(String relationship) {
		this.relationship = relationship;
	}

	public String getResetPasswordLink() {
		return resetPasswordLink;
	}

	public void setResetPasswordLink(String resetPasswordLink) {
		this.resetPasswordLink = resetPasswordLink;
	}

	/**
	 * @return the isApplicationUser
	 */
	public Boolean getIsApplicationUser() {
		return isApplicationUser;
	}

	/**
	 * @param isApplicationUser the isApplicationUser to set
	 */
	public void setIsApplicationUser(Boolean isApplicationUser) {
		this.isApplicationUser = isApplicationUser;
	}
}
