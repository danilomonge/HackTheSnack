package de.pecus.api.vo.product;

/**
 * 
 * @author Emilio Ribelles
 *
 *	Clase con los parametros de entrada a la invocacion del metodo 
 *  create de la case Recipe
 *
 */
public class DeleteProductIngredientRequestVO {


	// Identificador alfanumerico
	private Long idRecipe;
	// Identificador de producto
	private Long idProduct;
	// Identificador del ingrediente
	private Long idIngredient;


	public Long getIdRecipe() {return idRecipe;}
	public void setIdRecipe(Long idRecipe) {this.idRecipe = idRecipe;}

	public Long getIdProduct() {return idProduct;}
	public void setIdProduct(Long idProduct) {this.idProduct = idProduct;}

	public Long getIdIngredient() {return idIngredient;}
	public void setIdIngredient(Long idIngredient) {this.idIngredient = idIngredient;}


}
