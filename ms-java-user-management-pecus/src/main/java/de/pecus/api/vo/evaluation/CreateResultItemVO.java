package de.pecus.api.vo.evaluation;

import java.util.Date;

/**
 * 
 * @author Emilio Ribelles
 *
 *         Class with the ingredient result
 *
 */
public class CreateResultItemVO {


	private Long recipeId;
	private Long ingredientId;
	private Float ingredientMeanPercentage;
	private Float ingredientStdPercentage;

	public Long getRecipeId() {
		return recipeId;
	}
	public void setRecipeId(Long recipeId) {
		this.recipeId = recipeId;
	}

	public Long getIngredientId() {
		return ingredientId;
	}
	public void setIngredientId(Long ingredientId) {
		this.ingredientId = ingredientId;
	}

	public Float getIngredientMeanPercentage() { return this.ingredientMeanPercentage;}
	public void setIngredientMeanPercentage(Float ingredientMeanPercentage) {this.ingredientMeanPercentage = ingredientMeanPercentage;}

	public Float getIngredientStdPercentage() { return this.ingredientStdPercentage;}
	public void setIngredientStdPercentage(Float ingredientStdPercentage) {this.ingredientStdPercentage = ingredientStdPercentage;}

}
