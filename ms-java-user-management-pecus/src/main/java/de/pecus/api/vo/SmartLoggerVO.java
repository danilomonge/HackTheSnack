package de.pecus.api.vo;

import java.util.Date;

import com.fasterxml.jackson.annotation.JsonIgnore;

/**
 * SmartLoggerVO is a helper class to retrieve and store all the information
 * concerns to the logger
 * 
 * @author Juan Carlos Contreras Vazquez
 *
 */
public class SmartLoggerVO {

    private Class<?> clazz;

    private String methodName;

    private Date requestDateTime;

    @JsonIgnore
    private Date eventDate;

    private String token;

    public Class<?> getClazz() {
        return clazz;
    }

    public void setClazz(Class<?> clazz) {
        this.clazz = clazz;
    }

    public String getMethodName() {
        return methodName;
    }

    public void setMethodName(String methodName) {
        this.methodName = methodName;
    }

    public Date getRequestDateTime() {
        return requestDateTime;
    }

    public void setRequestDateTime(Date requestDateTime) {
        this.requestDateTime = requestDateTime;
    }

    public Date getEventDate() {
        return eventDate;
    }

    public void setEventDate(Date eventDate) {
        this.eventDate = eventDate;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }

}