package de.pecus.api.repositories.usuarios;

import java.io.Serializable;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import de.pecus.api.entities.EvaluationDO;

public interface EvaluationRepository extends JpaRepository<EvaluationDO, Serializable> {

	/**
	 * Query to recover an evaluation data
	 * 
	 * @return Objeto
	 * 
	 * @param id evaluation
	 */

	@Query(value = " SELECT r" 
			+ " FROM  EvaluationDO r"
			+ " JOIN FETCH r.brand b"
			+ " JOIN FETCH r.category c"
			+ " JOIN FETCH r.subCategory s"
			+ " JOIN FETCH r.product p"
			+ " JOIN FETCH r.ingredient i"
			+ " WHERE r.active = true "
			+ " AND r.id = :id")
	EvaluationDO findById(@Param("id") Long id);

	/**
	 * Query to recover the evaluation of a product
	 *
	 * @return List<Objeto> with the results
	 * 
	 * @param pageable
	 */

	@Query(value = " SELECT r"
			+ " FROM  EvaluationDO r"
			+ " JOIN FETCH r.brand b"
			+ " JOIN FETCH r.category c"
			+ " JOIN FETCH r.subCategory s"
			+ " JOIN FETCH r.product p"
			+ " JOIN FETCH r.ingredient i"
			+ " WHERE r.active = true "
			+ " AND r.product.id = :productId",
	countQuery="SELECT COUNT(r) "
			+ " FROM  EvaluationDO r "
			+ "	INNER JOIN r.brand b "
			+ " INNER JOIN r.category c "
			+ "	INNER JOIN r.subCategory s "
			+ "	WHERE r.active = true "
			+ " AND r.product.id = :productId")
	Page<EvaluationDO> findList(@Param("productId") Long productId,
                               Pageable pageable);

	}

