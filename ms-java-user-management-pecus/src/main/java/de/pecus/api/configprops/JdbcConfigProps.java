package de.pecus.api.configprops;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "jdbc")
public class JdbcConfigProps {

	private int initialPoolSize;
	private int acquireIncrement;
	private int minPoolSize;
	private int maxPoolSize;
	private int maxIdleTime;
	private int maxConnectionAge;
	private int maxIdleTimeExcessConnections;
	private int unreturnedConnectionTimeout;
	private int checkoutTimeout;
	private String contextClassLoaderSource;
	private boolean privilegeSpawnedThreads;
	private boolean debugUnreturnedConnectionStackTraces;
	
	public int getAcquireIncrement() {
		return acquireIncrement;
	}
	public void setAcquireIncrement(int acquireIncrement) {
		this.acquireIncrement = acquireIncrement;
	}
	public int getMinPoolSize() {
		return minPoolSize;
	}
	public void setMinPoolSize(int minPoolSize) {
		this.minPoolSize = minPoolSize;
	}
	public int getMaxPoolSize() {
		return maxPoolSize;
	}
	public void setMaxPoolSize(int maxPoolSize) {
		this.maxPoolSize = maxPoolSize;
	}
	public int getMaxIdleTime() {
		return maxIdleTime;
	}
	public void setMaxIdleTime(int maxIdleTime) {
		this.maxIdleTime = maxIdleTime;
	}
	public int getUnreturnedConnectionTimeout() {
		return unreturnedConnectionTimeout;
	}
	public void setUnreturnedConnectionTimeout(int unreturnedConnectionTimeout) {
		this.unreturnedConnectionTimeout = unreturnedConnectionTimeout;
	}
	/**
	 * @return the initialPoolSize
	 */
	public int getInitialPoolSize() {
		return initialPoolSize;
	}
	/**
	 * @param initialPoolSize the initialPoolSize to set
	 */
	public void setInitialPoolSize(int initialPoolSize) {
		this.initialPoolSize = initialPoolSize;
	}
	/**
	 * @return the maxConnectionAge
	 */
	public int getMaxConnectionAge() {
		return maxConnectionAge;
	}
	/**
	 * @param maxConnectionAge the maxConnectionAge to set
	 */
	public void setMaxConnectionAge(int maxConnectionAge) {
		this.maxConnectionAge = maxConnectionAge;
	}
	/**
	 * @return the maxIdleTimeExcessConnections
	 */
	public int getMaxIdleTimeExcessConnections() {
		return maxIdleTimeExcessConnections;
	}
	/**
	 * @param maxIdleTimeExcessConnections the maxIdleTimeExcessConnections to set
	 */
	public void setMaxIdleTimeExcessConnections(int maxIdleTimeExcessConnections) {
		this.maxIdleTimeExcessConnections = maxIdleTimeExcessConnections;
	}
	/**
	 * @return the checkoutTimeout
	 */
	public int getCheckoutTimeout() {
		return checkoutTimeout;
	}
	/**
	 * @param checkoutTimeout the checkoutTimeout to set
	 */
	public void setCheckoutTimeout(int checkoutTimeout) {
		this.checkoutTimeout = checkoutTimeout;
	}
	/**
	 * @return the contextClassLoaderSource
	 */
	public String getContextClassLoaderSource() {
		return contextClassLoaderSource;
	}
	/**
	 * @param contextClassLoaderSource the contextClassLoaderSource to set
	 */
	public void setContextClassLoaderSource(String contextClassLoaderSource) {
		this.contextClassLoaderSource = contextClassLoaderSource;
	}
	/**
	 * @return the privilegeSpawnedThreads
	 */
	public boolean getPrivilegeSpawnedThreads() {
		return privilegeSpawnedThreads;
	}
	/**
	 * @param privilegeSpawnedThreads the privilegeSpawnedThreads to set
	 */
	public void setPrivilegeSpawnedThreads(boolean privilegeSpawnedThreads) {
		this.privilegeSpawnedThreads = privilegeSpawnedThreads;
	}
	/**
	 * @return the debugUnreturnedConnectionStackTraces
	 */
	public boolean isDebugUnreturnedConnectionStackTraces() {
		return debugUnreturnedConnectionStackTraces;
	}
	/**
	 * @param debugUnreturnedConnectionStackTraces the debugUnreturnedConnectionStackTraces to set
	 */
	public void setDebugUnreturnedConnectionStackTraces(boolean debugUnreturnedConnectionStackTraces) {
		this.debugUnreturnedConnectionStackTraces = debugUnreturnedConnectionStackTraces;
	}
}
