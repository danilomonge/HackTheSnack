package de.pecus.api;

import java.util.ArrayList;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.concurrent.ConcurrentMapCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.EnableAspectJAutoProxy;
import org.springframework.context.annotation.aspectj.EnableSpringConfigured;
import org.springframework.context.support.PropertySourcesPlaceholderConfigurer;
import org.springframework.core.env.Environment;
import org.springframework.core.task.TaskExecutor;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import de.pecus.api.configprops.PecusDataSourceConfigProps;
import de.pecus.api.configprops.HibernateConfigProps;
import de.pecus.api.configprops.JdbcConfigProps;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.service.Contact;
import springfox.documentation.service.VendorExtension;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;


@SpringBootApplication(scanBasePackages = {"de.pecus.api"})
@EnableSwagger2
@EnableScheduling
@EnableAspectJAutoProxy(proxyTargetClass=true)
@EnableCaching
@EnableAsync
@EnableSpringConfigured
@EnableConfigurationProperties({
	HibernateConfigProps.class,
	PecusDataSourceConfigProps.class,
	JdbcConfigProps.class
})
public class MsJavaUserManagementPecusApplication {
	
	private static final String MICROSERVICE_CONTACT_EMAIL = "swagger.contact.email";
	private static final String MICROSERVICE_CONTACT_URL = "swagger.contact.url";
	private static final String MICROSERVICE_CONTACT_NAME = "swagger.contact.name";
	private static final String MICROSERVICE_DESCRIPTION = "swagger.description";
	private static final String MICROSERVICE_TITLE = "swagger.title";
	private static final String PROJECT_VERSION = "project.version";
	private static final String SWAGGER_ENABLED = "swagger.enabled";
	
	@Autowired
	private Environment env;
	
	public static void main(String[] args) {
		SpringApplication.run(MsJavaUserManagementPecusApplication.class, args);
	}
	
	protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
		return application.sources(MsJavaUserManagementPecusApplication.class);
	}
	
	@Bean
	public static PropertySourcesPlaceholderConfigurer placeHolderConfigurer() {
		return new PropertySourcesPlaceholderConfigurer();
	}

	@Bean
	public TaskExecutor taskExecutor() {
		ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
		executor.setCorePoolSize(5);
		executor.setMaxPoolSize(10);
		executor.setQueueCapacity(25);
		return executor;
	}
	
	/**
	 * Produces the information required by Swagger2 to render the Swagger-UI for
	 * the REST resvices published by the application.
	 *
	 * @return
	 */
	@Bean
	public Docket productApi() {
		return new Docket(DocumentationType.SWAGGER_2).select()
				.apis(RequestHandlerSelectors.basePackage("com.pecus.api.controllers")).paths(PathSelectors.any())
				.build().pathMapping("/").apiInfo(buildApiInfo()).useDefaultResponseMessages(false)
				.enable(Boolean.valueOf(env.getProperty(SWAGGER_ENABLED)));
	}

	@SuppressWarnings("rawtypes")
	private ApiInfo buildApiInfo() {
		return new ApiInfo(env.getProperty(MICROSERVICE_TITLE), env.getProperty(MICROSERVICE_DESCRIPTION),
				env.getProperty(PROJECT_VERSION), StringUtils.EMPTY/* termsOfServiceUrl */,
				new Contact(env.getProperty(MICROSERVICE_CONTACT_NAME), env.getProperty(MICROSERVICE_CONTACT_URL),
						env.getProperty(MICROSERVICE_CONTACT_EMAIL)),
				StringUtils.EMPTY/* license */, StringUtils.EMPTY/* licenseUrl */, new ArrayList<VendorExtension>());
	}

}
