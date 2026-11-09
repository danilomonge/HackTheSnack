package de.pecus.api.entities;

import java.io.Serializable;

import javax.persistence.MappedSuperclass;

/**
 * Clase base para mapeo de entidades
 * 
 * @author Luis Enrique Sanchez Santiago
 *
 * @param <I> Tipo generico que representa la llave primaria de la entidad
 */
@MappedSuperclass
public abstract class Base<I extends Serializable> implements Cloneable, Serializable {

    /** The Constant serialVersionUID. */
    private static final long serialVersionUID = 1L;
    
    /**
     * Gets the id.
     *
     * @return the id
     */
    public abstract I getId();

    /**
     * Sets the id.
     *
     * @param id the new id
     */
    
    public abstract void setId(I id);

    /**
     * Clone.
     *
     * @return the base do
     */
    @SuppressWarnings("unchecked")
    @Override
    public Base<I> clone() { // NOSONAR
    
        Base<I> baseDO = null;
        try {
            baseDO = (Base<I>)super.clone();
        }
        catch(Exception err) {
            baseDO = this;
        }
    
        return baseDO;
    }

}