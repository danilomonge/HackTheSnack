package de.pecus.api.services.usuarios;

import java.util.List;

import de.pecus.api.vo.RequestVO;
import de.pecus.api.vo.ResponseVO;
import de.pecus.api.vo.evaluation.CreateEvaluationRequestVO;
import de.pecus.api.vo.evaluation.FindDetailEvaluationRequestVO;
import de.pecus.api.vo.evaluation.FindDetailEvaluationResponseVO;
import de.pecus.api.vo.evaluation.FindListEvaluationRequestVO;
import de.pecus.api.vo.evaluation.FindListEvaluationResponseVO;


/**
 * Clase de logica de negocio para administracion de Evaluations
 * 
 * @author Proa
 *
 */
public interface EvaluationService {

	/**
	 * Crea un nuevo registro 
	 * 
	 * @param request Objeto con parametros de entrada 
	 * 
	 * @return Id generado
	 */
	ResponseVO<Long> create(RequestVO<CreateEvaluationRequestVO> request);
	

	/**
	 * Consulta un registro
	 *
	 * 
	 * @return Objeto VO con los datos encontrados
	 */
	ResponseVO<FindDetailEvaluationResponseVO> findDetail(RequestVO<FindDetailEvaluationRequestVO> request);

	
	/**
	 * Consulta la base de datos en base a varios parametros
	 * 
	 * @return ReponseVO con los datos encontrados
	 * 
	 * @param request Objeto con parametros de entrada 
	 */
	ResponseVO<List<FindListEvaluationResponseVO>> findList(RequestVO<FindListEvaluationRequestVO> request);



	/**
	 * Obtiene la lista de resultados para un producto y/o ingrediente
	 *
	 * @return ReponseVO con los datos encontrados
	 *
	 * @param request Objeto con parametros de entrada
	 */
	ResponseVO<List<FindListEvaluationResponseVO>> findListProductIngredientResult(RequestVO<FindListEvaluationRequestVO> request);


}
