/**
 * 
 */
package de.pecus.api.vo.usuarios;

/**
 * @author Luis Enrique Sanchez Santiago
 *
 */
public class updateUserEmailRequestVO {

	/** Correo del usuario **/
    private String oldEmail;
    /** Correo del usuario **/
    private String newEmail;
    /** Identificador del medico **/
    private Long idMedico;
    
	/**
	 * @return the oldEmail
	 */
	public String getOldEmail() {
		return oldEmail;
	}
	/**
	 * @param oldEmail the oldEmail to set
	 */
	public void setOldEmail(String oldEmail) {
		this.oldEmail = oldEmail;
	}
	/**
	 * @return the newEmail
	 */
	public String getNewEmail() {
		return newEmail;
	}
	/**
	 * @param newEmail the newEmail to set
	 */
	public void setNewEmail(String newEmail) {
		this.newEmail = newEmail;
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
