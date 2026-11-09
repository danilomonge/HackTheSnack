package de.pecus.api.vo.usuarios;

public class UpdatePasswordRequestVO {

	private String userId;
	
	private String newPassword;
	
	/** Flag para saber si es Mobile */
    private Boolean isMobile;

	public String getUserId() {
		return userId;
	}

	public void setUserId(String userId) {
		this.userId = userId;
	}

	/**
	 * @return the newPassword
	 */
	public String getNewPassword() {
		return newPassword;
	}

	/**
	 * @param newPassword the newPassword to set
	 */
	public void setNewPassword(String newPassword) {
		this.newPassword = newPassword;
	}

	/**
	 * @return the isMobile
	 */
	public Boolean getIsMobile() {
		return isMobile;
	}

	/**
	 * @param isMobile the isMobile to set
	 */
	public void setIsMobile(Boolean isMobile) {
		this.isMobile = isMobile;
	}

}
