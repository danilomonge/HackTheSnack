package de.pecus.api.entities;

import java.io.Serializable;

import javax.persistence.CascadeType;
import javax.persistence.FetchType;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.MappedSuperclass;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;

/**
 * Clase base para entidades que deban tener campo de idioma
 * 
 * @author Luis Enrique Sanchez Santiago
 *
 * @param <T> Tipo generico que representa la llave primaria de la entidad
 */
@MappedSuperclass
@JsonInclude(Include.NON_NULL)
public abstract class I18nBase<T extends Serializable> extends AuditBase<T> implements Cloneable, Serializable {

	private static final long serialVersionUID = -9069859860535192846L;
	
	/**************************** RELACION 1..N ******************************/
	@ManyToOne(fetch = FetchType.EAGER, cascade = { CascadeType.MERGE, CascadeType.DETACH })
	@JoinColumn(name = "FK_IDIOMA_ID", referencedColumnName = "PK_ID")
	private IdiomaDO idioma;

	public IdiomaDO getIdioma() {
		return idioma;
	}

	public void setIdioma(IdiomaDO idioma) {
		this.idioma = idioma;
	}
}
