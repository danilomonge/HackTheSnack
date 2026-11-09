/**
 * 
 */
package de.pecus.api.config;

import java.beans.PropertyVetoException;
import java.util.Properties;

import javax.persistence.EntityManagerFactory;
import javax.sql.DataSource;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.instrument.classloading.InstrumentationLoadTimeWeaver;
import org.springframework.orm.hibernate5.HibernateExceptionTranslator;
import org.springframework.orm.jpa.JpaTransactionManager;
import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import com.mchange.v2.c3p0.ComboPooledDataSource;

import de.pecus.api.configprops.HibernateConfigProps;
import de.pecus.api.configprops.JdbcConfigProps;
import de.pecus.api.configprops.PecusDataSourceConfigProps;
import de.pecus.api.error.GeneralBusinessErrors;
import de.pecus.api.exception.EnvironmentVariableNotFoundException;
import de.pecus.api.util.ValidatorUtil;

/**
 * 
 * Data access environment configuration class using Hibernate
 * @author pecus
 *
 */
@Configuration
@EnableTransactionManagement
@EnableJpaRepositories(basePackages = {"de.pecus.api.repositories", "de.pecus.api.security.repositories", "de.pecus.lib.repositories"})
public class PersistenceConfig {
    
    private static final Logger LOG = LoggerFactory.getLogger(PersistenceConfig.class);
    
    @Autowired
    private PecusDataSourceConfigProps pecusDataSourceConfigProps;
    
    @Autowired
    private HibernateConfigProps hibernateConfigProps;
    
    @Autowired
    private JdbcConfigProps jdbcConfigProps;
	
    @Bean
    public PlatformTransactionManager transactionManager() {
        EntityManagerFactory factory = entityManagerFactory().getObject();
        return new JpaTransactionManager( factory );
    }
	
    @Bean
    public LocalContainerEntityManagerFactoryBean entityManagerFactory() {
        LocalContainerEntityManagerFactoryBean factory = new LocalContainerEntityManagerFactoryBean();
	
        HibernateJpaVendorAdapter vendorAdapter = new HibernateJpaVendorAdapter();
	
        vendorAdapter.setGenerateDdl( false );
        vendorAdapter.setShowSql( hibernateConfigProps.getShowSql() );
	
        factory.setDataSource( dataSource() );
        factory.setJpaVendorAdapter( vendorAdapter );
        factory.setPackagesToScan( "de.pecus.api.entities" );
	
        Properties jpaProperties = new Properties();
        jpaProperties.put( "hibernate.hbm2ddl.auto", "none" );
        jpaProperties.put( "hibernate.dialect", hibernateConfigProps.getDialect() );
        jpaProperties.put( "hibernate.format_sql", "true" );
        jpaProperties.put( "hibernate.show_sql", hibernateConfigProps.getShowSql() );
        if(!ValidatorUtil.isNullOrEmpty(hibernateConfigProps.getDefaultSchema())) {
        	jpaProperties.put( "hibernate.default_schema", hibernateConfigProps.getDefaultSchema());
        }
        factory.setJpaProperties( jpaProperties );
  
        factory.afterPropertiesSet();
        factory.setLoadTimeWeaver( new InstrumentationLoadTimeWeaver() );
	
        return factory;
    }

    @Bean
    public HibernateExceptionTranslator hibernateExceptionTranslator() {
        return new HibernateExceptionTranslator();
    }
  
    @Bean(destroyMethod = "close")
    public DataSource dataSource() {
    	ComboPooledDataSource ds = new ComboPooledDataSource();
        try {
            ds.setDriverClass( pecusDataSourceConfigProps.getDriverClassName() );
            ds.setContextClassLoaderSource( jdbcConfigProps.getContextClassLoaderSource() );
        } catch (IllegalStateException | PropertyVetoException ex) {
            throw new RuntimeException("Error while setting the driver class name in the datasource", ex);
        } catch (EnvironmentVariableNotFoundException evnf) {
            LOG.error(GeneralBusinessErrors.NOT_FOUND_ENVIRONMENT_VAR, evnf);
        }
        ds.setJdbcUrl( pecusDataSourceConfigProps.getJdbcUrl() );
        ds.setUser( pecusDataSourceConfigProps.getUsername() );
        ds.setPassword( pecusDataSourceConfigProps.getPassword() );
        ds.setAcquireIncrement( jdbcConfigProps.getAcquireIncrement() );
        ds.setInitialPoolSize(jdbcConfigProps.getInitialPoolSize());
        ds.setMinPoolSize( jdbcConfigProps.getMinPoolSize() );
        ds.setMaxPoolSize( jdbcConfigProps.getMaxPoolSize() );
        ds.setMaxIdleTime( jdbcConfigProps.getMaxIdleTime() );
        if(!ValidatorUtil.isNull(ds.getMaxConnectionAge())) {
        	ds.setMaxConnectionAge( jdbcConfigProps.getMaxConnectionAge() );        	
        }
        if(!ValidatorUtil.isNull(jdbcConfigProps.getMaxIdleTimeExcessConnections())) {
        	ds.setMaxIdleTimeExcessConnections( jdbcConfigProps.getMaxIdleTimeExcessConnections() );
        }
        if(!ValidatorUtil.isNull(jdbcConfigProps.getUnreturnedConnectionTimeout())) {
        	ds.setUnreturnedConnectionTimeout( jdbcConfigProps.getUnreturnedConnectionTimeout() );
        }
        if(!ValidatorUtil.isNull(jdbcConfigProps.getPrivilegeSpawnedThreads())) {
        	ds.setPrivilegeSpawnedThreads( jdbcConfigProps.getPrivilegeSpawnedThreads() );
        }
        if(!ValidatorUtil.isNull(jdbcConfigProps.isDebugUnreturnedConnectionStackTraces())) {
        	ds.setDebugUnreturnedConnectionStackTraces(jdbcConfigProps.isDebugUnreturnedConnectionStackTraces());
        }

        return ds;
    	
    }
	
}
