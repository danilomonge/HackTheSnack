package de.pecus.api.vo.product;

import java.util.Date;

/**
 * 
 * @author Jose_Luis_Garcia
 *
 *         Clase con los parametros de entrada a la invocacion del metodo create
 *         de la case EventType
 *
 */
public class FindListProductRecipeResponseVO {

	// id
	private Long id;

	// Product
	private Long idProduct;
	private String nameProduct;

	// Ingredient
	private Long idIngredient;
	private String nameIngredient;

	//SubCategory
	private Date fechaRegistro;

	public Long getId() {
		return id;
	}
	public void setId(Long id) {this.id = id;}

	public Long getIdProduct() {
		return idProduct;
	}
	public void setIdProduct(Long idProduct) {
		this.idProduct = idProduct;
	}

	public String getNameProduct() {
		return nameProduct;
	}
	public void setNameProduct(String nameProduct) {
		this.nameProduct = nameProduct;
	}

	public Long getIdIngredient() {
		return idIngredient;
	}
	public void setIdIngredient(Long idIngredient) {
		this.idIngredient = idIngredient;
	}

	public String getNameIngredient() {
		return nameIngredient;
	}
	public void setNameIngredient(String nameIngredient) {
		this.nameIngredient = nameIngredient;
	}

}
