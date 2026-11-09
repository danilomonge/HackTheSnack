package de.pecus.api.configprops;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "hibernate")
public class HibernateConfigProps {

	private Boolean showSql;
	private String dialect;
	private String formatSql;
	@Value("${hibernate.hbm2ddl.auto}")
	private String hbm2dllAuto;
	private String defaultSchema;
	
	public Boolean getShowSql() {
		return showSql;
	}
	public void setShowSql(Boolean showSql) {
		this.showSql = showSql;
	}
	public String getDialect() {
		return dialect;
	}
	public void setDialect(String dialect) {
		this.dialect = dialect;
	}
	public String getFormatSql() {
		return formatSql;
	}
	public void setFormatSql(String formatSql) {
		this.formatSql = formatSql;
	}
	public String getHbm2dllAuto() {
		return hbm2dllAuto;
	}
	public void setHbm2dllAuto(String hbm2dllAuto) {
		this.hbm2dllAuto = hbm2dllAuto;
	}
	/**
	 * @return the defaultSchema
	 */
	public String getDefaultSchema() {
		return defaultSchema;
	}
	/**
	 * @param defaultSchema the defaultSchema to set
	 */
	public void setDefaultSchema(String defaultSchema) {
		this.defaultSchema = defaultSchema;
	}
}
