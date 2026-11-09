package de.pecus.api.entities;

import java.io.Serializable;
import java.util.Date;

import javax.persistence.Column;
import javax.persistence.MappedSuperclass;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;

/**
 * Clase base para entidades que deban tener campos de control y auditoria
 * 
 * @author Luis Enrique Sanchez Santiago
 *
 * @param <T> Tipo generico que representa la llave primaria de la entidad
 */
@MappedSuperclass
public abstract class AuditBase<T extends Serializable> extends Base<T> implements Cloneable, Serializable {

    private static final long serialVersionUID = -9069859860535192846L;

    @Column(name = "DN_USUARIO_MODIFICADOR", nullable = true)
    protected Long lastModifiedUsername;

    @Column(name = "DD_FECHA_MODIFICACION", nullable = true)
    @Temporal(TemporalType.TIMESTAMP)
    protected Date lastModifiedDate;

    @Column(name = "DN_USUARIO_CREADOR", nullable = false)
    protected Long creatorUsername;

    @Column(name = "DD_FECHA_CREACION", nullable = false)
    @Temporal(TemporalType.TIMESTAMP)
    protected Date creationDate;
    
    @Column(name = "DN_ACTIVO", nullable = false)
    protected Boolean active;

    /**
     * Gets the last modified username.
     *
     * @return the last modified username
     */

    public Long getLastModifiedUsername() {
        return lastModifiedUsername;
    }

    /**
     * Sets the last modified username.
     *
     * @param newVal the new last modified username
     */
    public void setLastModifiedUsername( Long newVal ) {
        lastModifiedUsername = newVal;
    }

    /**
     * Gets the last modified date.
     *
     * @return the last modified date
     */
    public Date getLastModifiedDate() {
        if( lastModifiedDate != null ){
            return (Date) lastModifiedDate.clone();
        }
        return null;
    }

    /**
     * Sets the last modified date.
     *
     * @param newVal the new last modified date
     */
    public void setLastModifiedDate( Date newVal ) {
        if( newVal != null ){
            lastModifiedDate = (Date) newVal.clone();
        }
        else{
            lastModifiedDate = null;
        }
    }

    /**
     * Gets the last modified username.
     *
     * @return the last modified username
     */
    public Long getCreatorUsername() {
        return creatorUsername;
    }

    /**
     * Sets the last modified username.
     *
     * @param newVal the new last modified username
     */
    public void setCreatorUsername( Long newVal ) {
        creatorUsername = newVal;
    }

    /**
     * Gets the last modified date.
     *
     * @return the last modified date
     */
    public Date getCreationDate() {
        if( creationDate != null ){
            return (Date) creationDate.clone();
        }
        return null;
    }

    /**
     * Sets the last modified date.
     *
     * @param newVal the new last modified date
     */
    public void setCreationDate( Date newVal ) {
        if( newVal != null ){
            creationDate = (Date) newVal.clone();
        }
        else{
            creationDate = null;
        }
    }

    /**
     * @return the active
     */
    public Boolean getActive() {
        return active;
    }

    /**
     * @param active the active to set
     */
    public void setActive(Boolean active) {
        this.active = active;
    }
}