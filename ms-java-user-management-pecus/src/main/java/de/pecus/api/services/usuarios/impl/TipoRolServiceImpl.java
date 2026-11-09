package de.pecus.api.services.usuarios.impl;

import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.domain.Sort.Direction;
import org.springframework.stereotype.Service;
import org.apache.commons.lang.math.RandomUtils;

import de.pecus.api.constant.DataConstants;
import de.pecus.api.entities.TipoRolDO;
import de.pecus.api.enums.WildcardTypeEnum;
import de.pecus.api.error.FuncionesBusinessError;
import de.pecus.api.error.GeneralBusinessErrors;
import de.pecus.api.repositories.usuarios.TipoRolRepository;
import de.pecus.api.services.usuarios.TipoRolService;
import de.pecus.api.util.CriteriaUtil;
import de.pecus.api.util.ResponseUtil;
import de.pecus.api.util.ServiceUtil;
import de.pecus.api.util.StringUtil;
import de.pecus.api.util.ValidatorArqUtil;
import de.pecus.api.util.ValidatorUtil;
import de.pecus.api.vo.RequestVO;
import de.pecus.api.vo.ResponseVO;
import de.pecus.api.vo.roles.CreateTipoRolRequestVO;
import de.pecus.api.vo.roles.DeleteTipoRolRequestVO;
import de.pecus.api.vo.roles.FindDetailTipoRolRequestVO;
import de.pecus.api.vo.roles.FindDetailTipoRolResponseVO;
import de.pecus.api.vo.roles.FindListTipoRolRequestVO;
import de.pecus.api.vo.roles.FindListTipoRolResponseVO;
import de.pecus.api.vo.roles.UpdateTipoRolRequestVO;

/**
 * Clase de logica de negocio para administracion de tipoRoles
 * 
 * @author Proa
 *
 */
@Service
public class TipoRolServiceImpl implements TipoRolService {

	@Autowired
	private TipoRolRepository tipoRolRepository;


	/**
	 * Crea un nuevo registro de tipoRol
	 * 
	 * @param request Objeto con parametros de entrada de tipoRol
	 * 
	 * @return Id generado
	 */
	public ResponseVO<Long> create(RequestVO<de.pecus.api.vo.roles.CreateTipoRolRequestVO> request) {

		// Declarar variables
		ResponseVO<Long> response = new ResponseVO<>();
		
			// Validar los parametros de entrada
			if (validateParametersCreate(request, response)) {
		
				// Preparar los datos para actualizar la BB.DD.
				TipoRolDO tipoRolDO = new TipoRolDO();
				
				tipoRolDO.setId(RandomUtils.nextLong());
				tipoRolDO.setIdNombre(request.getParameters().getIdNombre());
				tipoRolDO.setDescripcion(request.getParameters().getDescripcion());
				tipoRolDO.setGlobal(request.getParameters().getGlobal());
				
				// Actualizar los parametros de auditoria
				ServiceUtil.setAuditFields(tipoRolDO, request.getToken());

				// Insertar el registro
				tipoRolDO = tipoRolRepository.saveAndFlush(tipoRolDO);

				// Regresar la respuesta correcta y el objeto a regresar
				response.setSuccess(true);
				response.setData(tipoRolDO.getId());
				
			}
		return response;
	}


	/**
	 * Actualiza un registro de tipoRol
	 * 
	 * @param request Objeto con parametros de entrada de tipoRol
	 * 
	 * @return Id actualizado
	 */
	public ResponseVO<Long> update(RequestVO<UpdateTipoRolRequestVO> request) {

		// Declarar variables
		ResponseVO<Long> response = new ResponseVO<>();
		TipoRolDO registroDO = new TipoRolDO();

		// Validar los campos de entrada
		if (validateParametersUpdate(request, response)) {
			
			UpdateTipoRolRequestVO parameters = request.getParameters();

			registroDO.setId(parameters.getId());
			registroDO.setIdNombre(parameters.getIdNombre());
			registroDO.setDescripcion(parameters.getDescripcion());
			registroDO.setGlobal(parameters.getGlobal());
			
			// Actualizar parametros de auditoria
			ServiceUtil.setAuditFields(registroDO, request.getToken());

			// Actualizar el registro en BB.DD.
			registroDO = tipoRolRepository.saveAndFlush(registroDO);

			// Preparar respuesta y objeto actualizado
			response.setSuccess(true);
			response.setData(registroDO.getId());
		}
		return response;
	}


	/**
	 * Marca un registro como eliminado un registro de tipoRol
	 * 
	 * @param request Objeto con parametros de entrada de tipoRol
	 * 
	 * @return Id eliminado
	 */
	public ResponseVO<Boolean> delete(RequestVO<DeleteTipoRolRequestVO> request) {

		// Declarar variables
		ResponseVO<Boolean> response = new ResponseVO<>();

		// Validar campos de entrada
		if (validateParametersDelete(request, response)) {

			TipoRolDO tipoRolDO = this.exists(request.getParameters().getId(), null);
			if (ValidatorUtil.isNull(tipoRolDO)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_ERROR, request);
			}
			else {
			// Actualizar la informacion
			ServiceUtil.setDisabledEntity(tipoRolDO, request.getToken());
			
			// Actualizar la BB.DD.
			tipoRolDO = tipoRolRepository.saveAndFlush(tipoRolDO);

			// Preparar respuesta y objeto eliminado
			response.setSuccess(true);
			response.setData(Boolean.TRUE);
			}
		}
		return response;
	}

	/**
	 * Consulta un tipoRol por Identificador unico
	 * 
	 * @return Objeto VO con los datos encontrados
	 * @param Id      Identificador del registro a buscar
	 * 
	 * @param request Objeto con los datos de busqueda
	 */
	public ResponseVO<FindDetailTipoRolResponseVO> findDetail(RequestVO<FindDetailTipoRolRequestVO> request) {

		// declaracion de varables
		ResponseVO<FindDetailTipoRolResponseVO> response = new ResponseVO<>();
		FindDetailTipoRolResponseVO salida = new FindDetailTipoRolResponseVO();
		
		// validar que se cumplen las condiciones para realizar la consulta
		if (validateParametersFindDetail(request, response)) {

			TipoRolDO tipoRolDO = this.exists(request.getParameters().getId(), request.getParameters().getIdNombre());

			if (ValidatorUtil.isNull(tipoRolDO)) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_ERROR, request);
			} else {
				salida.setId(tipoRolDO.getId());
				salida.setIdNombre(tipoRolDO.getIdNombre());
				salida.setDescripcion(tipoRolDO.getDescripcion());
				salida.setGlobal(tipoRolDO.getGlobal());

				response.setData(salida);
				// regresar la respuesta correcta con los registros obtenidos.
				response.setSuccess(true);
			}
				
		}
			
		return response;
	}



	
	/**
	 * Consulta la base de datos en base a varios parametros
	 * 
	 * @return ReponseVO con los datos encontrados
	 * 
	 * @param request Objeto con parametros de entrada de banner
	 */
	public ResponseVO<List<FindListTipoRolResponseVO>> findList(RequestVO<FindListTipoRolRequestVO> request) {

		// declaracion de varables
		ResponseVO<List<FindListTipoRolResponseVO>> response = new ResponseVO<>();
		
		Page<TipoRolDO> listaTipoRol = null;
		
		if (validateParametersFindByList(request, response)) {
	
			FindListTipoRolRequestVO parameters = request.getParameters();
			// Se obtiene el idioma
			
			String  idNombre 	= CriteriaUtil.validateNullLike(parameters.getIdNombre(), WildcardTypeEnum.BOTH_SIDES);
			
			// Preparamos el objeto para la paginacion
			String orderby = request.getOrderBy();
			String ordertype = request.getOrderType();
			String orderBy = ValidatorUtil.isNullOrEmpty(orderby) ? "id" : orderby;
			Direction orderType = ValidatorUtil.isNullOrEmpty(ordertype) || ordertype.equals("asc") ? Direction.ASC
					: Direction.DESC;
			Integer size = ValidatorUtil.isNullOrZero(request.getSize()) ? 10 : request.getSize();
			Integer page = ValidatorUtil.isNullOrZero(request.getPage()) ? 1 : request.getPage();
			Pageable pageable = PageRequest.of(page - 1, size, Sort.by(orderType, orderBy));
			
			String normalizedIdNombre = this.limpiarAcentos(request.getParameters().getIdNombre());
			
			// ejecucion de la busqueda por el parametro recibido
			listaTipoRol = tipoRolRepository.findList(this.cleanString(normalizedIdNombre), pageable);

			// Si no se encontro ningun registro que cumpla la condicion generar error.
			if (ValidatorUtil.isNullOrEmpty(listaTipoRol.getContent())) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_REGISTER_LIST_ERROR);
			} else {
				// Regresar la respuesta correcta con los registros obtenidos.
				response.setSuccess(true);
				response.setTotalRows(listaTipoRol.getTotalElements());
				response.setData(transformListDO(listaTipoRol.getContent()));
			}
		}
		return response;
	}
	

	
	/*******************************************************************************************************
	 * 
	 * FIN METODOS PUBLICOS
	 * 
	 *******************************************************************************************************/

	/*******************************************************************************************************
	 * 
	 * METODOS VALIDACION
	 * 
	 *******************************************************************************************************/

	/**
	 * Valida que los parametros para la operacion de insercion sean correctos
	 * 
	 * @param request  Objeto con los parametros de entrada
	 * @param response Respuesta donde se agregan los errores
	 * @return true si todos los parametros son correctos
	 */
	private boolean validateParametersCreate(RequestVO<CreateTipoRolRequestVO> request, ResponseVO<Long> response) {
		
		// Obtener los parametros de entrada
		CreateTipoRolRequestVO parameters = request.getParameters();

		// Validaciones de campos obligatorios
		if (StringUtil.isNullOrEmpty(parameters.getIdNombre())) {
			ResponseUtil.addError(request, response, 
					FuncionesBusinessError.REQUIRED_ID_NOMBRE_ERROR, request);
		} else {
			// Validacion de tamano
			String idNombre = StringUtil.substring(parameters.getIdNombre(), DataConstants.MAX_SIZE_ID_NOMBRE);

			// Validacion de formato
			parameters.setIdNombre(StringUtil.toUpperCase(idNombre));

				TipoRolDO registroB = this.exists(null,parameters.getIdNombre());
				
				if (!ValidatorUtil.isNull(registroB)) {
					ResponseUtil.addError(request, response, 
							FuncionesBusinessError.DUPLICATED_ERROR, request);					
			}
		}
		
		// Validaciones de campos obligatorios
		if (StringUtil.isNullOrEmpty(parameters.getDescripcion())) {
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_DESCRIPCION_ERROR,request);
		} else {
			// Validacion de tamano
			parameters.setDescripcion(StringUtil.substring(parameters.getDescripcion(), DataConstants.MAX_SIZE_DESCRIPCION));
		}
		
		if (ValidatorUtil.isNull(parameters.getGlobal())) {
			request.getParameters().setGlobal(false);
		}
				
		// Regresar el resultado de la validacion
		return ValidatorUtil.isSuccessfulResponse(response);
	}


	/**
	 * Valida que los parametros para la operacion de actualizacion sean correctos
	 * 
	 * @param request  Objeto con los parametros de entrada
	 * @param response Respuesta donde se agregan los errores
	 * @return true si todos los parametros son correctos
	 */
	private boolean validateParametersUpdate(RequestVO<UpdateTipoRolRequestVO> request, ResponseVO<Long> response) {
		// Recuperar parametros de entrada
		UpdateTipoRolRequestVO parameters = request.getParameters();
		TipoRolDO registroUpdate = new TipoRolDO();
		
		// Validar que se informaron los campos de entrada
		if (ValidatorUtil.isNull(parameters)) {
			// Si no se ha informado regresar el error y no seguir validando
			ResponseUtil.addError(request, response, GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR);
			return false;
		}
		
		//Validar que exista el registro a actualizar
		if(ValidatorUtil.isNull(parameters.getId()))
		{
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_ERROR, request);
			return false;
		} else {
			
				registroUpdate = this.exists(parameters.getId(),null);
			
				if (ValidatorUtil.isNull(registroUpdate)) {
					ResponseUtil.addError(request, response, FuncionesBusinessError.NOT_FOUND_ERROR, request);
					return false;
				}
		}
		
		// Validaciones de campos obligatorios: NOMBRE
		if (!StringUtil.isNullOrEmpty(parameters.getIdNombre())) {
			// Validacion de tamano
			String idNombre = StringUtil.substring(parameters.getIdNombre(), DataConstants.MAX_SIZE_ID_NOMBRE);

			// Validacion de formato
			parameters.setIdNombre(StringUtil.toUpperCase(idNombre));
			
				//Validar la posible duplicidad del idNombre
				TipoRolDO tipoRolBusqueda = this.exists(null, request.getParameters().getIdNombre());
				
				if (!ValidatorUtil.isNull(tipoRolBusqueda)) {
					//Si se encuentra el registro validamos que no sea el mismo Id
					if (registroUpdate.getId() != tipoRolBusqueda.getId()) {
						ResponseUtil.addError(request, response, FuncionesBusinessError.DUPLICATED_ERROR, request);
						
					}
			}
		} else {
			parameters.setIdNombre(registroUpdate.getIdNombre());
		}
		
		// Validaciones de campos obligatorios: DESCRIPCION
		if (!StringUtil.isNullOrEmpty(parameters.getDescripcion())) {
			// Validacion de tamano
			parameters.setDescripcion(
					StringUtil.substring(parameters.getDescripcion(), DataConstants.MAX_SIZE_DESCRIPCION));

		} else {
			parameters.setDescripcion(registroUpdate.getDescripcion());
		}
			
		if (ValidatorUtil.isNull(parameters.getGlobal())) {
			parameters.setGlobal(registroUpdate.getGlobal());
		}
		
		// Retorna el resultado de la validacion.
		return ValidatorUtil.isSuccessfulResponse(response);
		
	}

	/**
	 * Valida que los parametros para la operacion de eliminacion sean correctos
	 * 
	 * @param request  Objeto con los parametros de entrada
	 * @param response Respuesta donde se agregan los errores
	 * @return true si todos los parametros son correctos
	 */
	private boolean validateParametersDelete(RequestVO<DeleteTipoRolRequestVO> request, ResponseVO<Boolean> response) {

		// Validar que se han informado los parametros de entrada
		if (ValidatorUtil.isNull(request.getParameters())) {
			// Si no se han informado generar error y terminar de validar
			ResponseUtil.addError(request, response, GeneralBusinessErrors.REQUIRED_PARAMETERS_ERROR);
			return false;
		}

		// Validaciones de campos obligatorios
		if (ValidatorUtil.isNullOrZero(request.getParameters().getId())) {
			ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_ERROR);
		}
		
		return ValidatorUtil.isSuccessfulResponse(response);
	}


	/**
	 * Valida que los parametros para la operacion de consulta por nombre sean
	 * correctos
	 * 
	 * @param Id Identificador del registro a buscar
	 * @return true si el nombre no esta vacio
	 * 
	 * @param request  Objeto con los parametros a valida
	 * @param response Respuesta donde se agregan los errores
	 */
	private boolean validateParametersFindDetail(RequestVO<FindDetailTipoRolRequestVO> request, ResponseVO<FindDetailTipoRolResponseVO> response) {

		// Recuperar los parametros de entrada
		FindDetailTipoRolRequestVO parameters = request.getParameters();

		// validar que el campo obligatorio
		if (ValidatorUtil.isNullOrZero(parameters.getId())) {
			
			//Buscar por criterio: IdNombre
			if (ValidatorUtil.isNullOrEmpty(parameters.getIdNombre())) {
				ResponseUtil.addError(request, response, FuncionesBusinessError.REQUIRED_ID_ERROR);
			} 
		}
		
		return ValidatorUtil.isSuccessfulResponse(response);
	}


	/**
	 * Valida que los parametros para la operacion de consulta por parametros sean
	 * correctos
	 * 
	 * @return true si el nombre no esta vacio
	 * 
	 * @param request  Objeto con los criterios a buscar
	 * @param response Respuesta donde se agregan los errores
	 */
	private boolean validateParametersFindByList(RequestVO<FindListTipoRolRequestVO> request,
			ResponseVO<List<FindListTipoRolResponseVO>> response) {
		
		// Validar campos obligatorios
	    ValidatorArqUtil.validateParameters(request, response);
		
		// validar los parametros de la paginacion
	    ValidatorArqUtil.validatePaginatonParameters(request, response);
		return ValidatorUtil.isSuccessfulResponse(response);

	}



	/**
	 * Obtiene una lista de objetos tipoRolVO a partir de una lista de DO
	 * 
	 * @return Lista VO para retorno de resultados
	 * 
	 * @param listaTipoRol a transformar
	 */
	private List<FindListTipoRolResponseVO> transformListDO(List<TipoRolDO> listaTipoRol) {

		// Declarar variables
		List<FindListTipoRolResponseVO> listaTipoRolVO = new ArrayList<>();

		// recorrer el objeto origen
		for (TipoRolDO tipoRolDO : listaTipoRol) {
			// Se hace la declaracion de variables necesarias
			FindListTipoRolResponseVO tipoRolVO = new FindListTipoRolResponseVO();
			
			tipoRolVO.setId(tipoRolDO.getId());
			tipoRolVO.setIdNombre(tipoRolDO.getIdNombre());
			tipoRolVO.setDescripcion(tipoRolDO.getDescripcion());
			tipoRolVO.setGlobal(tipoRolDO.getGlobal());
			
			listaTipoRolVO.add(tipoRolVO);
		}

		return listaTipoRolVO;
	}
	


	/*************************************************************************
	 * Metodo que busca un registro por su id, idNombre
	 * Regresa el objeto de la base de datos o una excepcion con el error
	 * 
	 *************************************************************************/
	public TipoRolDO exists(Long id, String idNombre){

		TipoRolDO registro = null;
		try {
			//Validacion de datos de entrada
			if (ValidatorUtil.isNullOrZero(id)) {
				if (ValidatorUtil.isNullOrEmpty(idNombre)) {
					registro = null;
				} else {
					//Buscamos por nombre
					registro = tipoRolRepository.findByIdNombre(idNombre);
				}
			} else {
				//Consulta
				registro = tipoRolRepository.findById(id);
			}
			//Validacion de existencia
			if (ValidatorUtil.isNull(registro)) {
				//Genera error
				registro = null;
			}
		} catch (Exception e) {
			registro = null;
		}
		
		return registro;
	}	



	public String cleanString(String strInput) {
		if(!ValidatorUtil.isNullOrEmpty(strInput)) {
			strInput = strInput.trim().toUpperCase();
		}
		return strInput; 
	}
	
	public String limpiarAcentos(String cadena) {
	    String limpio =null;
	    if (cadena !=null) {
	        String valor = cadena;
	        valor = valor.toUpperCase();
	        // Normalizar texto para eliminar acentos, dieresis, cedillas y tildes
	        limpio = Normalizer.normalize(valor, Normalizer.Form.NFD);
	        // Quitar caracteres no ASCII excepto la enie, interrogacion que abre, exclamacion que abre, grados, U con dieresis.
	        limpio = limpio.replaceAll("[^\\p{ASCII}(N\u0303)(n\u0303)(\u00A1)(\u00BF)(\u00B0)(U\u0308)(u\u0308)]", "");
	        // Regresar a la forma compuesta, para poder comparar la enie con la tabla de valores
	        limpio = Normalizer.normalize(limpio, Normalizer.Form.NFC);
	    }
	    return limpio;
	}
	
	
}
