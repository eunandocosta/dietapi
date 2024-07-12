from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from database import init_db, SessionLocal
from models.model import Dieta, Refeicao, Alimento
from schemas.schema import RefeicaoCreate, DietaCreate, AlimentoCreate
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from logs.log_config import setup_logging

logger = setup_logging()

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

init_db(app)

@app.route('/dietas', methods=['POST'])
def create_dieta():
    session = SessionLocal()
    data = request.get_json()

    try:
        dieta_data = DietaCreate(**data)
    except ValidationError as e:
        logger.error("Erro de validação ao criar dieta: %s", e.errors())
        return jsonify(e.errors()), 400

    try:
        nova_dieta = Dieta(firebase_uuid=dieta_data.firebase_uuid)
        session.add(nova_dieta)
        session.commit()
        session.refresh(nova_dieta)

        for refeicao_data in dieta_data.refeicoes:
            nova_refeicao = Refeicao(tipo=refeicao_data.tipo, dieta_id=nova_dieta.id)
            session.add(nova_refeicao)
            session.commit()
            session.refresh(nova_refeicao)

            for alimento_data in refeicao_data.alimentos:
                novo_alimento = Alimento(
                    nome=alimento_data.nome,
                    quantidade=alimento_data.quantidade,
                    refeicao_id=nova_refeicao.id
                )
                session.add(novo_alimento)

        session.commit()
        logger.info("Dieta criada com sucesso: %s", nova_dieta.to_dict())
        return jsonify(nova_dieta.to_dict())
    except IntegrityError as e:
        logger.error("Erro de integridade ao criar dieta: %s", str(e))
        session.rollback()
        return jsonify({"error": "Erro de integridade ao criar dieta"}), 500
    except Exception as e:
        logger.error("Erro desconhecido ao criar dieta: %s", str(e))
        session.rollback()
        return jsonify({"error": "Erro desconhecido ao criar dieta"}), 500
    
@app.route('/delete_dietas', methods=['DELETE'])
def delete_dietas():
    session = SessionLocal()
    data = request.get_json()
    firebase_uuid = data.get('firebase_uuid')

    if not firebase_uuid:
        return jsonify({"error": "UUID do Firebase é necessário"}), 400

    try:
        dieta = session.query(Dieta).filter_by(firebase_uuid=firebase_uuid).first()
        if not dieta:
            return jsonify({"error": "Nenhuma dieta encontrada para o UUID fornecido"}), 404

        # Deletar todas as refeições e alimentos associados
        refeicoes = session.query(Refeicao).filter_by(dieta_id=dieta.id).all()
        for refeicao in refeicoes:
            alimentos = session.query(Alimento).filter_by(refeicao_id=refeicao.id).all()
            for alimento in alimentos:
                session.delete(alimento)
            session.delete(refeicao)

        session.delete(dieta)
        session.commit()
        logger.info(f"Todas as dietas para o UUID {firebase_uuid} foram deletadas com sucesso.")
        return jsonify({'message': 'Todas as dietas deletadas com sucesso'}), 200
    except Exception as e:
        logger.error(f"Erro ao deletar dietas para o UUID {firebase_uuid}: {str(e)}")
        session.rollback()
        return jsonify({'error': 'Erro ao deletar dietas'}), 500


@app.route('/dieta', methods=['GET'])
def get_dieta():
    session = SessionLocal()
    firebase_uuid = request.args.get('firebase_uuid')
    if not firebase_uuid:
        return jsonify({"error": "UUID do Firebase é necessário"}), 400

    try:
        dieta = session.query(Dieta).filter_by(firebase_uuid=firebase_uuid).first()
        if not dieta:
            return jsonify({"error": "Nenhuma dieta encontrada para o UUID fornecido"}), 404
        logger.info("Dieta encontrada para firebase_uuid %s", firebase_uuid)
        return jsonify(dieta.to_dict())
    except Exception as e:
        logger.error("Erro ao buscar dieta: %s", str(e))
        return jsonify({"error": "Erro ao buscar dieta"}), 500

@app.route('/dietas/<int:id>', methods=['DELETE'])
def delete_dieta(id):
    session = SessionLocal()
    dieta = session.query(Dieta).filter_by(id=id).first()
    if not dieta:
        return jsonify({'error': 'Dieta não encontrada'}), 404

    try:
        session.delete(dieta)
        session.commit()
        logger.info(f"Dieta com ID {id} deletada com sucesso.")
        return jsonify({'message': 'Dieta deletada com sucesso'}), 200
    except Exception as e:
        logger.error(f"Erro ao deletar a dieta com ID {id}: {str(e)}")
        session.rollback()
        return jsonify({'error': 'Erro ao deletar a dieta'}), 500
    
@app.route('/update_quantidade', methods=['PUT'])
def update_quantidade():
    session = SessionLocal()
    data = request.get_json()
    alimento_id = data.get('alimento_id')
    nova_quantidade = data.get('nova_quantidade')
    
    try:
        alimento = session.query(Alimento).filter_by(id=alimento_id).first()
        if not alimento:
            return jsonify({'error': 'Alimento não encontrado'}), 404
        
        alimento.quantidade = nova_quantidade
        session.commit()
        logger.info("Quantidade do alimento atualizada com sucesso: %s", alimento.to_dict())
        return jsonify(alimento.to_dict())
    except Exception as e:
        logger.error("Erro ao atualizar a quantidade do alimento: %s", str(e))
        session.rollback()
        return jsonify({'error': 'Erro ao atualizar a quantidade do alimento'}), 500

@app.route('/delete_alimento', methods=['DELETE'])
def delete_alimento():
    session = SessionLocal()
    data = request.get_json()
    alimento_id = data.get('alimento_id')
    
    try:
        alimento = session.query(Alimento).filter_by(id=alimento_id).first()
        if not alimento:
            return jsonify({'error': 'Alimento não encontrado'}), 404
        
        session.delete(alimento)
        session.commit()
        logger.info("Alimento deletado com sucesso")
        return jsonify({'message': 'Alimento deletado com sucesso'}), 200
    except Exception as e:
        logger.error("Erro ao deletar o alimento: %s", str(e))
        session.rollback()
        return jsonify({'error': 'Erro ao deletar o alimento'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
