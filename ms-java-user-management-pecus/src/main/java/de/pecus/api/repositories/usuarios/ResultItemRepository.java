package de.pecus.api.repositories.usuarios;

import java.io.Serializable;
import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import de.pecus.api.entities.ResultItemDO;

public interface ResultItemRepository extends JpaRepository<ResultItemDO, Serializable> {

	/**
	 * Consulta por id un resultado
	 * 
	 * @return Objeto de mapeo a la entidad
	 * 
	 * @param id Identificador de registro buscado
	 */
	@Query(value = " SELECT r" 
			+ " FROM  ResultItemDO r"
			+ " WHERE r.active = true "
			+ " AND r.id = :id")
	ResultItemDO findById(@Param("id") Long id);
	
	/**
	 * Consultala lista de resultados de una Evaluación con paginacion
	 * 
	 * @return List<Objeto> con el resultado
	 * 
	 * @param pageable
	 */

	@Query(value = " SELECT r" 
			+ " FROM  ResultItemDO r"
			+ " WHERE r.active = true "
			+ " AND r.evaluation.id	= :idEvaluation",
			countQuery="SELECT COUNT(r) "
					+ " FROM  ResultItemDO r "
					+ " WHERE r.active = true "
					+ " AND r.evaluation.id =:idEvaluation")
	Page<ResultItemDO> findList(@Param("idEvaluation") Long idEvaluation,
                               Pageable pageable);

	/**
	 * Consulta la lista de resultados de una evaluacion sin paginacion
	 *
	 * @return List<Objeto> con el resultado
	 *
	 */

	@Query(value = " SELECT r"
			+ " FROM  ResultItemDO r"
			+ " JOIN FETCH r.ingredient i"
			+ " WHERE r.active = true "
			+ " AND r.evaluation.id	= :id")
	List<ResultItemDO> findAllResult(@Param("id") Long id);

	/**
	 * Consulta la lista de resultados de un producto ordenada por fecha ascendente
	 * (o id evaluación ascendente), con paginación, con los filtros producto, ingrediente o ambos
	 *
	 * @return List<Objeto> con el resultado
	 *
	 */

	@Query(value = " SELECT r"
			+ " FROM  ResultItemDO r"
			+ " JOIN FETCH r.product p"
			+ " JOIN FETCH r.ingredient i"
//			+ " JOIN FETCH r.product.brand b"
//			+ " JOIN FETCH r.product.category c"
//			+ " JOIN FETCH r.product.subCategory sc"
			+ " WHERE r.active = true "
			+ " AND (:idProduct IS NULL OR r.product.id = :idProduct)"
			+ " AND (:idIngredient IS NULL OR r.ingredient.id = :idIngredient)",
			countQuery="SELECT COUNT(r) "
					+ " FROM  ResultItemDO r "
					+ " INNER JOIN r.product p"
					+ " INNER JOIN r.ingredient i"
//					+ " INNER JOIN r.product.brand b"
//					+ " INNER JOIN r.product.category c"
//					+ " INNER JOIN r.product.subCategory sc"
					+ " WHERE r.active = true "
					+ " AND (:idProduct IS NULL OR r.product.id = :idProduct)"
					+ " AND (:idIngredient IS NULL OR r.ingredient.id = :idIngredient)")
	Page<ResultItemDO> findListProductIngredientResult(
						@Param("idProduct") Long idProduct,
						@Param("idIngredient") Long idIngredient,
						Pageable pageable);



}
