package de.pecus.api.vo.evaluation;

/**
 * 
 * @author Emilio Ribelles
 *
 * Data entry to recover a list of evaluation for a product, results of a product and result of an ingredient
 * Each funtion takes the right parameter
 */
public class FindListEvaluationRequestVO {

	//Product Id
	private Long idProduct;

	//Product Id
	private Long idIngredient;


	public Long getIdProduct() {
		return idProduct;
	}
	public void setIdProduct(Long idProduct) {
		this.idProduct = idProduct;
	}

	public Long getIdIngredient() {
		return idIngredient;
	}
	public void setIdIngredient(Long idIngredient) {
		this.idIngredient = idIngredient;
	}


}
