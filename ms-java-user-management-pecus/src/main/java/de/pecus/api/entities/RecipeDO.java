package de.pecus.api.entities;

/******************** SECCION IMPORTS ***************************************/

import javax.persistence.*;
import java.io.Serializable;
import java.util.Date;

/**
 * Catalog Recipe
 * 
 * List of Recipe registered in the systema.
 * @author jose.ribelles
 * @version 1.0
 * @created 24-jul.-2019 11:27:46 a. m.
 */
@Entity
@Table(name = "RECIPE")
public class RecipeDO extends AuditBase<Long> implements Serializable {

	private static final long serialVersionUID = -5382607608047169433L;

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name="PK_ID")
	private Long id;

	/****************************  RELACION 1..N ******************************/
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "FK_PRODUCT_ID" , referencedColumnName = "PK_ID")
	private ProductDO product;

	/****************************  RELACION 1..N ******************************/
	@ManyToOne (fetch = FetchType.LAZY)
	@JoinColumn(name = "FK_INGREDIENT_ID" , referencedColumnName = "PK_ID")
	private IngredientDO ingredient;

	@Column(name="DD_REGISTER_DATE")
	private Date fechaRegistro;


	public RecipeDO(){

	}

	public void finalize() throws Throwable {

	}

	public Long getId() {
		return id;
	}
	public void setId(Long id) {
		this.id = id;
	}

	public ProductDO getProduct() {
		return product;
	}
	public void setProduct(ProductDO id) {
		this.product = id;
	}

	public IngredientDO getIngredient() {
		return ingredient;
	}
	public void setIngredient(IngredientDO id) {
		this.ingredient = id;
	}

	public Date getFechaRegistro() { return this.fechaRegistro;}
	public void setFechaRegistro(Date fechaRegistro) {this.fechaRegistro = fechaRegistro;}

}