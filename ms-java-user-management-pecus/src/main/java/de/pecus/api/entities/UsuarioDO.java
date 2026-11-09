package de.pecus.api.entities;

/******************** SECCION IMPORTS ***************************************/
import java.io.Serializable;
import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;

/******************** FIN SECCION IMPORTS ************************************/

/**
 * Usuario podria ser el mail o el telefono.
 * 
 * 
 * Con el telefono podriamos empatar con la agenda de contactos del usuario para
 * que al seleccionar algun usuario supieramos si la otra persona tiene PECUS o
 * no.
 * 
 * @author jose_
 * @version 1.0
 * @created 24-jul.-2019 11:27:46 a. m.
 */
@Entity
@Table(name = "USUARIO")
public class UsuarioDO extends AuditBase<Long> implements Serializable {

    /**
     * Serial Version
     */
    private static final long serialVersionUID = 3736839829404032486L;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="PK_ID")
    private Long id;
    
	@Temporal(TemporalType.TIMESTAMP)
    @Column(name = "DD_LAST_LOGIN")
    private Date lastLoginActive;
    @Column(name = "DN_NOTIFICATION_ENABLED")
    private Boolean notificationsEnabled;
    @Column(name = "DX_PASSWORD")
    private String password;
    @Column(name = "DN_PASSWORD_STATUS")
    private Integer passwordStatus;
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "DD_PASSWORD_STATUS_CHANGE")
    private Date passwordStatusChangedAt;
    @Column(name = "DD_REFRESH_TOKEN_DATE")
    private Date refreshTokenExpeditionTime;
    @Column(name = "DX_REFRESH_PREVIOUS_TOKEN")
    private String refreshPreviousToken;
    @Column(name = "DX_REFRESH_TOKEN_TOKEN")
    private String refreshTokenToken;
    @Column(name = "DX_USER_ID_EMAIL")
    private String userIdEmail;
    @Column(name = "DX_USER_ID_DEVICE")
    private String userIdMobileDevice;
    @Column(name = "DX_USER_ID_MOBILE")
    private String userIdMobileNumber;
    @Column(name = "DX_IMAGEN_PERFIL")
    private String imagenPerfil;
    @Column(name = "DX_FIREBASE_TOKEN")
    private String pushProviderToken;
    @Column(name = "DX_USER_ID_PAIS")
    private String ladaPais;
    @Column(name = "DD_ACEPTACION_TERMINOS" )
    private Date terminosAceptados;
    @Column(name = "DX_CODIGO_ALEXA")
    private String codigoAlexa;
    
    public UsuarioDO() {

    }

    public void finalize() throws Throwable {

    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }


    public Date getLastLoginActive() {
        return lastLoginActive;
    }

    public void setLastLoginActive(Date lastLoginActive) {
        this.lastLoginActive = lastLoginActive;
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

    public Integer getPasswordStatus() {
        return passwordStatus;
    }

    public void setPasswordStatus(Integer passwordStatus) {
        this.passwordStatus = passwordStatus;
    }

    public Date getPasswordStatusChangedAt() {
        return passwordStatusChangedAt;
    }

    public void setPasswordStatusChangedAt(Date passwordStatusChangedAt) {
        this.passwordStatusChangedAt = passwordStatusChangedAt;
    }

    public Date getRefreshTokenExpeditionTime() {
        return refreshTokenExpeditionTime;
    }

    public void setRefreshTokenExpeditionTime(Date refreshTokenExpeditionTime) {
        this.refreshTokenExpeditionTime = refreshTokenExpeditionTime;
    }

    public String getRefreshPreviousToken() {
        return refreshPreviousToken;
    }

    public void setRefreshPreviousToken(String refreshPreviousToken) {
        this.refreshPreviousToken = refreshPreviousToken;
    }

    public String getRefreshTokenToken() {
        return refreshTokenToken;
    }

    public void setRefreshTokenToken(String refreshTokenToken) {
        this.refreshTokenToken = refreshTokenToken;
    }

    public String getUserIdEmail() {
        return userIdEmail;
    }

    public void setUserIdEmail(String userIdEmail) {
        this.userIdEmail = userIdEmail;
    }

    public String getUserIdMobileDevice() {
        return userIdMobileDevice;
    }

    public void setUserIdMobileDevice(String userIdMobileDevice) {
        this.userIdMobileDevice = userIdMobileDevice;
    }

    public String getUserIdMobileNumber() {
        return userIdMobileNumber;
    }

    public void setUserIdMobileNumber(String userIdMobileNumber) {
        this.userIdMobileNumber = userIdMobileNumber;
    }

    public String getImagenPerfil() {
        return imagenPerfil;
    }

    public void setImagenPerfil(String imagenPerfil) {
        this.imagenPerfil = imagenPerfil;
    }

    public String getPushProviderToken() {
        return pushProviderToken;
    }

    public void setPushProviderToken(String pushProviderToken) {
        this.pushProviderToken = pushProviderToken;
    }

    public String getLadaPais() {
        return ladaPais;
    }

    public void setLadaPais(String ladaPais) {
        this.ladaPais = ladaPais;
    }

	public Date getTerminosAceptados() {
		return terminosAceptados;
	}

	public void setTerminosAceptados(Date terminosAceptados) {
		this.terminosAceptados = terminosAceptados;
	}

	public String getCodigoAlexa() {
		return codigoAlexa;
	}

	public void setCodigoAlexa(String codigoAlexa) {
		this.codigoAlexa = codigoAlexa;
	}

    public Boolean isNotificationsEnabled() {
        return this.notificationsEnabled;
    }

}