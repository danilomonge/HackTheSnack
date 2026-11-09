package de.pecus.api.vo.evaluation;


import java.util.Date;
import java.util.List;

/**
 * 
 * @author Emilio Ribelles
 *
 *	Data entry to save an evaluation
 *
 */
public class CreateEvaluationRequestVO {

	//Product
	private Long idProduct;

	//Ingredient with percentage
	private Long idIngredient;
	// Relation id between product and ingredient
	private Long idRecipe;

	// Ingredient mean precentaje
	private Float ingredientMeanPercentage;

	// Ingredient variation precentaje
	private Float ingredientStdPercentage;

	//Evaluation Date.
	private Date evaluationDate;

	//List of results
	private List<CreateResultItemVO> resultList;

	public Long getIdProduct() {
		return idProduct;
	}
	public void setIdProduct(Long id) {
		this.idProduct = id;
	}

	public Long getIdIngredient() {
		return idIngredient;
	}
	public void setIdIngredient(Long id) {
		this.idIngredient = id;
	}

	public Long getIdRecipe() {
		return idRecipe;
	}
	public void setIdRecipe(Long id) {
		this.idRecipe = id;
	}

	public Float getIngredientMeanPercentage() {
		return ingredientMeanPercentage;
	}
	public void setIngredientMeanPercentage(Float id) {
		this.ingredientMeanPercentage = id;
	}

	public Float getIngredientStdPercentage() {
		return ingredientStdPercentage;
	}
	public void setIngredientStdPercentage(Float id) {
		this.ingredientStdPercentage = id;
	}

	public Date getEvaluationDate() {
		return evaluationDate;
	}
	public void setEvaluationDate(Date evaluationDate) {
		this.evaluationDate = evaluationDate;
	}
	
	public List<CreateResultItemVO> getResultList() {return resultList;}
	public void setResultList(List<CreateResultItemVO> resultList) {this.resultList = resultList;}
}
