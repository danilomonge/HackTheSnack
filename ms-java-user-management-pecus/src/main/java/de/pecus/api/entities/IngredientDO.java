package de.pecus.api.entities;

/******************** SECCION IMPORTS ***************************************/

import javax.persistence.*;
import java.io.Serializable;

/**
 * Catalog Ingredient
 * 
 * List of Ingredient registered in the systema.
 * @author jose.ribelles
 * @version 1.0
 * @created 24-jul.-2019 11:27:46 a. m.
 */
@Entity
@Table(name = "INGREDIENT")
public class IngredientDO extends AuditBase<Long> implements Serializable {

	/**
	 *
	 */
	private static final long serialVersionUID = -5382607608047169433L;

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name="PK_ID")
	private Long id;
	@Column(name =  "DX_NAME" )
	private String name;
	@Column(name =  "DX_DESCRIPTION" )
	private String description;


	public IngredientDO(){

	}

	public void finalize() throws Throwable {

	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}
}