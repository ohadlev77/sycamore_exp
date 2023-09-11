"""TODO COMPLETE."""

from qiskit_ibm_provider import IBMProvider

from src.qiskit_rcs_v2.mine_v1_5q_rcs_data import export_execution_res


if __name__ == "__main__":

    provider = IBMProvider()

    jakarta_job = provider.retrieve_job("cir4c0tlipn2bcc0ce90")
    nairobi_job = provider.retrieve_job("cir5ratlipn2bcc1evpg")

    export_execution_res(
        jakarta_job,
        filepath="/home/ohad/work/sycamore_exp_project/src/qiskit_rcs_v2/" \
            "exp_data__ibmq_jakarta/ibmq_jakarta_counts.json"
    )

    export_execution_res(
        nairobi_job,
        filepath="/home/ohad/work/sycamore_exp_project/src/qiskit_rcs_v2/" \
            "exp_data__ibm_nairobi/ibm_nairobi_counts.json"
    )