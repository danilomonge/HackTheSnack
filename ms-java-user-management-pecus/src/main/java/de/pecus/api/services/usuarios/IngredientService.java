package de.pecus.api.services.usuarios;

import java.util.List;

import de.pecus.api.vo.RequestVO;
import de.pecus.api.vo.ResponseVO;
import de.pecus.api.vo.ingredient.CreateIngredientRequestVO;
import de.pecus.api.vo.ingredient.DeleteIngredientRequestVO;
import de.pecus.api.vo.ingredient.FindDetailIngredientRequestVO;
import de.pecus.api.vo.ingredient.FindDetailIngredientResponseVO;
import de.pecus.api.vo.ingredient.FindListIngredientRequestVO;
import de.pecus.api.vo.ingredient.FindListIngredientResponseVO;
import de.pecus.api.vo.ingredient.UpdateIngredientRequestVO;

/**
 * Clase de logica de negocio para administracion de Ingredientes
 * 
 * @author Proa
 *
 */
public interface IngredientService {

	/**
	 * Crea un nuevo registro 
	 * 
	 * @param request Objeto con parametros de entrada 
	 * 
	 * @return Id generado
	 */
	ResponseVO<Long> create(RequestVO<CreateIngredientRequestVO> request);

	/**
	 * Actualiza un registro 
	 * 
	 * @param request Objeto con parametros de entrada 
	 * 
	 * @return Id actualizado
	 */
	ResponseVO<Long> update(RequestVO<UpdateIngredientRequestVO> request);

	/**
	 * Marca un registro como eliminado un registro 
	 * 
	 * @param request Objeto con parametros de entrada 
	 * 
	 * @return Id eliminado
	 */
	ResponseVO<Boolean> delete(RequestVO<DeleteIngredientRequestVO> request);

	/**
	 * Consulta un registro
	 * 
	 * @param numero Nombre  buscado
	 * 
	 * @return Objeto VO con los datos encontrados
	 */
	ResponseVO<FindDetailIngredientResponseVO> findDetail(RequestVO<FindDetailIngredientRequestVO> request);

	
	/**
	 * Consulta la base de datos en base a varios parametros
	 * 
	 * @return ReponseVO con los datos encontrados
	 * 
	 * @param request Objeto con parametros de entrada 
	 */
	ResponseVO<List<FindListIngredientResponseVO>> findList(RequestVO<FindListIngredientRequestVO> request);



}
