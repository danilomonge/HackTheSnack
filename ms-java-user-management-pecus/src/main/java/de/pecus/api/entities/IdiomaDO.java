package de.pecus.api.entities;

/******************** SECCION IMPORTS ***************************************/
import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
/******************** FIN SECCION IMPORTS ************************************/

/**
 * @author jorge.serrano
 * @version 1.0
 * @created 23-mayo.-2019 09:31:29 p. m.
 */
@Entity
@Table(name = "IDIOMA")
public class IdiomaDO extends AuditBase<Long> implements Serializable {

	/**
	 * Serial Version
	 */
	private static final long serialVersionUID = 2923329749134816615L;

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name =  "PK_ID" )
	private Long id;
	
	@Column(name =  "DX_ID_NOMBRE" )
	private String idNombre;
	
	@Column(name =  "DX_DESCRIPCION" )
	private String descripcion;

	public IdiomaDO(){
		// por defecto viene vacio el metodo
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getIdNombre() {
		return idNombre;
	}

	public void setIdNombre(String idNombre) {
		this.idNombre = idNombre;
	}

	public String getDescripcion() {
		return descripcion;
	}

	public void setDescripcion(String descripcion) {
		this.descripcion = descripcion;
	}
}
