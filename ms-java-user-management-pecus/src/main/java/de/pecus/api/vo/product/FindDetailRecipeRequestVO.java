package de.pecus.api.vo.product;

/**
 * 
 * @author Emilio Ribelles Mairn
 *
 *	Clase con los parametros de entrada a la invocacion del metodo 
 *  findDetail de la case Recipe
 *
 */
public class FindDetailRecipeRequestVO {


	// Identificador de registro
	private Long id;

	// Identificador del producto
	private Long idProduct;

	// Identificador del ingrediente
	private Long idIngredient;

	public Long getId() {
		return id;
	}
	public void setId(Long id) {
		this.id = id;
	}

	public Long getIdProduct() { return idProduct; }
	public void setIdProduct(Long idProduct) {this.idProduct = idProduct; }

	public long getIdIngredient() { return idIngredient; }
	public void setIdIngredient(long idIngredient) {this.idIngredient = idIngredient; }

}
