package de.pecus.api.repositories.usuarios;

import java.io.Serializable;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import de.pecus.api.entities.TipoRolDO;

public interface TipoRolRepository extends JpaRepository<TipoRolDO, Serializable> {

	/**
	 * Consulta por idNombre sin implementacion de query especifico
	 * @param idNombre Identificador de nombre buscado
	 * @return Objeto de mapeo a la entidad
	 */
	@Query(value = " SELECT r" 
			+ " FROM  TipoRolDO r"
			+ " WHERE r.active = true "
			+ " AND r.idNombre = :idNombre")
	TipoRolDO findByIdNombre(@Param("idNombre") String idNombre);
	
	/**
	 * Consulta por id sin implementacion de query especifico
	 * 
	 * @return Objeto de mapeo a la entidad
	 * 
	 * @param id Identificador de registro buscado
	 */
	@Query(value = " SELECT r" 
			+ " FROM  TipoRolDO r"
			+ " WHERE r.active = true "
			+ " AND r.id = :id")
	TipoRolDO findById(@Param("id") Long id);
	
    /**
	 * Consulta por nombre . Y se prepara para paginacion
	 * 
	 * @return List<Objeto> con el resultado
	 * 
	 * @param idNombre cadena descriptiva de registro buscado
	 * @param pageable
	 */
	@Query(value = " SELECT r" 
			+ " FROM  TipoRolDO r"
			+ " WHERE r.active = true "
			+ " AND (:idNombre IS NULL OR (TRANSLATE(UPPER(r.idNombre),'áéíóú','aeiou') LIKE %:idNombre%))")
	Page<TipoRolDO> findList(@Param("idNombre") String idNombre, 
			Pageable pageable);
	
}
