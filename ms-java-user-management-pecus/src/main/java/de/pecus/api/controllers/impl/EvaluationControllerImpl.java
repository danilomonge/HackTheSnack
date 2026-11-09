package de.pecus.api.controllers.impl;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import de.pecus.api.controllers.EvaluationController;
import de.pecus.api.services.usuarios.EvaluationService;
import de.pecus.api.util.EvaluationServicesResponseBuilder;
import de.pecus.api.util.RequestVOUtil;
import de.pecus.api.util.ResponseUtil;
import de.pecus.api.vo.RequestVO;
import de.pecus.api.vo.ResponseVO;
import de.pecus.api.vo.evaluation.CreateEvaluationRequestVO;
import de.pecus.api.vo.evaluation.FindDetailEvaluationRequestVO;
import de.pecus.api.vo.evaluation.FindDetailEvaluationResponseVO;
import de.pecus.api.vo.evaluation.FindListEvaluationRequestVO;
import de.pecus.api.vo.evaluation.FindListEvaluationResponseVO;
import io.swagger.annotations.ApiImplicitParam;
import io.swagger.annotations.ApiImplicitParams;

/**
 * Clase de controlador para servicio Rest de Evaluation
 * 
 * @author Emilio Ribelles
 * @version 1.0
 * @created 13-jun-2025 11:34:31 a. m.
 */
@RestController
@RequestMapping("")
public class EvaluationControllerImpl implements EvaluationController {

	//public static final SmartLogger LOGGER = SmartLoggerFactory.getLogger(EvaluationController.class);

	@Autowired
	private EvaluationService evaluationService;

	/**
	 * Operation: Operation: create, Method: POST Crea un registro en la BB.DD.
	 * @param headers		Arreglo de objetos de tipo llave valor para almacenar los headers
	 * @param body 			Cuerpo de la peticion con la informacion del regsitro que se desean insertar
	 * @return 				Ojeto con el cuerpo de respuesta (ong con el id del registro actualizado) y le codigo de respuesta http corrspondiente a la operacion
	 */
	@Override
	@ApiImplicitParams({
		@ApiImplicitParam(name = "Authorization", value = "eyJhbGciOiJIUzI1NiJ9.eyJUT0tFTl9EQVRBIjp7ImFwZWxs", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "mac-address", value = " 2C:54:91:88:C9:E3 or 2c-54-91-88-c9-e3", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "request-date", value = "2021-09-07 17:29:25.443", paramType = "header", dataTypeClass = String.class, required = true),
		@ApiImplicitParam(name = "latitude", value = "-74.00898606", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "longitude", value = "40.71727401", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "language", value = "es_MX", paramType = "header", dataTypeClass = String.class, required = true),
		@ApiImplicitParam(name = "time-zone", value = "America/Mexico City", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "id-client-invoke", value = "21", paramType = "header", dataTypeClass = String.class, required = true),
		@ApiImplicitParam(name = "client-operation-code", value = "qWERGFDSRSGfsdertRTRe2345RTd", paramType = "header", dataTypeClass = String.class, required = true) })
	@PostMapping(value = "/evaluation", produces = MediaType.APPLICATION_JSON_VALUE)
	public ResponseEntity<ResponseVO<Long>> createEvaluation(@RequestHeader Map<String, String> headers,
			@RequestBody CreateEvaluationRequestVO body) {
		
			// Generamos el objeto requestVO
			RequestVO<CreateEvaluationRequestVO> requestVO = RequestVOUtil.setNewRequestVO(headers,body);

			ResponseEntity<ResponseVO<Long>> response = null;
			try {
				// Invocar al servicio
				ResponseVO<Long> serviceResponse = evaluationService.create(requestVO);

				response  = EvaluationServicesResponseBuilder.buildCreateOrUpdateResponse(serviceResponse);

			} catch (Exception exception) {
				// Excepcion controlada
				ResponseVO<Long> exceptionResponse = ResponseUtil.getErrorResponse(exception);
				response = ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(exceptionResponse);
			}
			return response;
			
	}
	
	/**
	 * Operation: findEventDetail, Method: Busca el detalle de un registro en la base de datos.
	 * 
	 * @param headers		Arreglo de objetos de tipo llave valor para almacenar los headers
	 * @param id 			Identificador del registro a buscar
	 * @return 				Objeto con el resultado del borrado
	 */
	@Override
	@ApiImplicitParams({
		@ApiImplicitParam(name = "Authorization", value = "eyJhbGciOiJIUzI1NiJ9.eyJUT0tFTl9EQVRBIjp7ImFwZWxs", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "mac-address", value = " 2C:54:91:88:C9:E3 or 2c-54-91-88-c9-e3", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "request-date", value = "2021-09-07 17:29:25.443", paramType = "header", dataTypeClass = String.class, required = true),
		@ApiImplicitParam(name = "latitude", value = "-74.00898606", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "longitude", value = "40.71727401", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "language", value = "es_MX", paramType = "header", dataTypeClass = String.class, required = true),
		@ApiImplicitParam(name = "time-zone", value = "America/Mexico City", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "id-client-invoke", value = "21", paramType = "header", dataTypeClass = String.class, required = true),
		@ApiImplicitParam(name = "client-operation-code", value = "qWERGFDSRSGfsdertRTRe2345RTd", paramType = "header", dataTypeClass = String.class, required = true) })
	@GetMapping(value = "/evaluation/detail", produces = MediaType.APPLICATION_JSON_VALUE)
	public ResponseEntity<ResponseVO<FindDetailEvaluationResponseVO>> findDetailEvaluation(
			@RequestHeader Map<String, String> headers, 
			@RequestParam(value = "id", required= false) Long id) {

		// Declaracion de variables
		ResponseEntity<ResponseVO<FindDetailEvaluationResponseVO>> response = null;

		// Crear el objeto requestVO
		FindDetailEvaluationRequestVO findDetailEvaluationRequestVO = new FindDetailEvaluationRequestVO();
		findDetailEvaluationRequestVO.setId(id);

		RequestVO<FindDetailEvaluationRequestVO> requestVO = RequestVOUtil.setNewRequestVO(headers,findDetailEvaluationRequestVO);

		try {
			
			// Invocar al metodo de busqueda
			ResponseVO<FindDetailEvaluationResponseVO> serviceResponse = evaluationService.findDetail(requestVO);
			
			response = EvaluationServicesResponseBuilder.buildFindDetailResponse(serviceResponse);

		} catch (Exception exception) {
			// Excepcion no controlada
			ResponseVO<FindDetailEvaluationResponseVO> exceptionResponse = ResponseUtil.getErrorResponse(exception);
			response = ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(exceptionResponse);
		}
		return response;
	}
	
	/**
	 * Operation: findEvaluationList, Method: GET Consulta la lista de registros en
	 * base a varios parametros. El resultado se regresa como un arreglo de
	 * registros.
	 * 
	 * @return ResponseVO con la lista de registros encontrada
	 * 
	 * @param page   Numero de pagina
	 * @param size   Tamano de pagina
	 */
	@Override
	@ApiImplicitParams({
		@ApiImplicitParam(name = "Authorization", value = "eyJhbGciOiJIUzI1NiJ9.eyJUT0tFTl9EQVRBIjp7ImFwZWxs", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "mac-address", value = " 2C:54:91:88:C9:E3 or 2c-54-91-88-c9-e3", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "request-date", value = "2021-09-07 17:29:25.443", paramType = "header", dataTypeClass = String.class, required = true),
		@ApiImplicitParam(name = "latitude", value = "-74.00898606", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "longitude", value = "40.71727401", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "language", value = "es_MX", paramType = "header", dataTypeClass = String.class, required = true),
		@ApiImplicitParam(name = "time-zone", value = "America/Mexico City", paramType = "header", dataTypeClass = String.class),
		@ApiImplicitParam(name = "id-client-invoke", value = "21", paramType = "header", dataTypeClass = String.class, required = true),
		@ApiImplicitParam(name = "client-operation-code", value = "qWERGFDSRSGfsdertRTRe2345RTd", paramType = "header", dataTypeClass = String.class, required = true) })
	@GetMapping(value = "/evaluation/list", produces = MediaType.APPLICATION_JSON_VALUE)
	public ResponseEntity<ResponseVO<List<FindListEvaluationResponseVO>>> findListEvaluation(
			@RequestHeader Map<String, String> headers, 
			@RequestParam(value = "page", required = false) Integer page,
			@RequestParam(value = "size", required = false) Integer size,
			@RequestParam(value = "orderBy", required = false) String orderBy,
			@RequestParam(value = "orderType", required = false) String orderType,
			@RequestParam(value = "idProduct", required = false) Long idProduct){
		// Declarar variables
		ResponseEntity<ResponseVO<List<FindListEvaluationResponseVO>>> response = null;

		FindListEvaluationRequestVO findListEvaluationRequestVO = new FindListEvaluationRequestVO();
		findListEvaluationRequestVO.setIdProduct(idProduct);
		RequestVO<FindListEvaluationRequestVO> requestVO = RequestVOUtil.setNewRequestVO(headers, page, size, orderBy,
				orderType, findListEvaluationRequestVO);

		try {
			
			ResponseVO<List<FindListEvaluationResponseVO>> serviceResponse = evaluationService.findList(requestVO);
			response = EvaluationServicesResponseBuilder.buildFindListEvaluationResponse(serviceResponse);

		} catch (Exception exception) {
			// Excepcion no controlada
			ResponseVO<List<FindListEvaluationResponseVO>> exceptionResponse = ResponseUtil
					.getErrorResponse(exception);
			response = ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(exceptionResponse);
		}
		return response;
	}

	/**
	 * Operation: findEvaluationList, Method: GET Consulta la lista de registros en
	 * base a varios parametros. El resultado se regresa como un arreglo de
	 * registros.
	 *
	 * @return ResponseVO con la lista de registros encontrada
	 *
	 * @param page   Numero de pagina
	 * @param size   Tamano de pagina
	 */
	@Override
	@ApiImplicitParams({
			@ApiImplicitParam(name = "Authorization", value = "eyJhbGciOiJIUzI1NiJ9.eyJUT0tFTl9EQVRBIjp7ImFwZWxs", paramType = "header", dataTypeClass = String.class),
			@ApiImplicitParam(name = "mac-address", value = " 2C:54:91:88:C9:E3 or 2c-54-91-88-c9-e3", paramType = "header", dataTypeClass = String.class),
			@ApiImplicitParam(name = "request-date", value = "2021-09-07 17:29:25.443", paramType = "header", dataTypeClass = String.class, required = true),
			@ApiImplicitParam(name = "latitude", value = "-74.00898606", paramType = "header", dataTypeClass = String.class),
			@ApiImplicitParam(name = "longitude", value = "40.71727401", paramType = "header", dataTypeClass = String.class),
			@ApiImplicitParam(name = "language", value = "es_MX", paramType = "header", dataTypeClass = String.class, required = true),
			@ApiImplicitParam(name = "time-zone", value = "America/Mexico City", paramType = "header", dataTypeClass = String.class),
			@ApiImplicitParam(name = "id-client-invoke", value = "21", paramType = "header", dataTypeClass = String.class, required = true),
			@ApiImplicitParam(name = "client-operation-code", value = "qWERGFDSRSGfsdertRTRe2345RTd", paramType = "header", dataTypeClass = String.class, required = true) })
	@GetMapping(value = "/evaluation/listResult", produces = MediaType.APPLICATION_JSON_VALUE)
	public ResponseEntity<ResponseVO<List<FindListEvaluationResponseVO>>> findListProductIngredientResult(
			@RequestHeader Map<String, String> headers,
			@RequestParam(value = "page", required = false) Integer page,
			@RequestParam(value = "size", required = false) Integer size,
			@RequestParam(value = "orderBy", required = false) String orderBy,
			@RequestParam(value = "orderType", required = false) String orderType,
			@RequestParam(value = "idProduct", required = false) Long idProduct,
			@RequestParam(value = "idIngredient", required = false) Long idIngredient)
	{
		// Declarar variables
		ResponseEntity<ResponseVO<List<FindListEvaluationResponseVO>>> response = null;

		FindListEvaluationRequestVO findListEvaluationRequestVO = new FindListEvaluationRequestVO();
		findListEvaluationRequestVO.setIdProduct(idProduct);
		findListEvaluationRequestVO.setIdIngredient(idIngredient);

		RequestVO<FindListEvaluationRequestVO> requestVO = RequestVOUtil.setNewRequestVO(headers, page, size, orderBy,
				orderType, findListEvaluationRequestVO);

		try {

			ResponseVO<List<FindListEvaluationResponseVO>> serviceResponse = evaluationService.findListProductIngredientResult(requestVO);
			response = EvaluationServicesResponseBuilder.buildFindListEvaluationResponse(serviceResponse);

		} catch (Exception exception) {
			// Excepcion no controlada
			ResponseVO<List<FindListEvaluationResponseVO>> exceptionResponse = ResponseUtil
					.getErrorResponse(exception);
			response = ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(exceptionResponse);
		}
		return response;
	}

}