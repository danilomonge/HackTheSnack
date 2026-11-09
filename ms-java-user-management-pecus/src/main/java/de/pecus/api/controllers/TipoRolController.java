package de.pecus.api.controllers;

import java.util.List;
import java.util.Map;

import org.springframework.http.ResponseEntity;

import de.pecus.api.vo.ResponseVO;
import de.pecus.api.vo.roles.CreateTipoRolRequestVO;
import de.pecus.api.vo.roles.FindDetailTipoRolResponseVO;
import de.pecus.api.vo.roles.FindListTipoRolResponseVO;
import de.pecus.api.vo.roles.UpdateTipoRolRequestVO;

public interface TipoRolController {

	/**
	 * Servicio para crear un registro.
	 * 
	 * @param headers 		Cabeceras de la solicitud.
	 * @param idNombre		Id alfanumerico del registro
	 * @param descripcion	Descripcion del registro
	 * 
	 * @return Responde una entidad de tipo Response el registro creado
	 */
	ResponseEntity<ResponseVO<Long>> createTipoRol(Map<String, String> headers, CreateTipoRolRequestVO body);

	/**
	 * Servicio para actualiza un registro.
	 * 
	 * @param headers 		Cabeceras de la solicitud.
	 * @param id			Id del registro a actualizar
	 * @param idNombre		Id alfanumerico del registro
	 * @param descripcion	Descripcion del registro
	 * 
	 * @return Responde una entidad de tipo Response el registro actualizado
	 */
	ResponseEntity<ResponseVO<Long>> updateTipoRol(Map<String, String> headers, Long id, UpdateTipoRolRequestVO body);

	/**
	 * Servicio para elimina un registro.
	 * 
	 * @param headers 		Cabeceras de la solicitud.
	 * @param id			Id del registro a actualizar
	 * 
	 * @return Responde una entidad de tipo Response el booleano del resultado
	 */
	ResponseEntity<ResponseVO<Boolean>> deleteTipoRol(Map<String, String> headers, Long id);

	/**
	 * Servicio consulta un registro
	 * 
	 * @param headers 		Cabeceras de la solicitud.
	 * @param id			Id del registro a actualizar
	 * @param idNombre		Id alfanumerico del registro
	 * 
	 * @return Responde una entidad de tipo Response con los datos del registro
	 */
	ResponseEntity<ResponseVO<FindDetailTipoRolResponseVO>> findDetailTipoRol(Map<String, String> headers, Long id, String idNombre);

	
	/**
	 * Servicio para consulta de los datos de la tabla con filtros
	 * 
	 * @param headers 		Cabeceras de la solicitud.
	 * @param idNombre		Id alfanumerico del registro
	 * 
	 * @return Responde una lista de registros encontrados
	 */
	ResponseEntity<ResponseVO<List<FindListTipoRolResponseVO>>> findListTipoRol(Map<String, String> headers,Integer page,
			Integer size, String orderBy,String orderType,  String idNombre);


	
	
}
