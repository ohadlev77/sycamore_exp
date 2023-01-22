OPENQASM 2.0;
include "qelib1.inc";
qreg q[16];
creg c[16];
id q[1];
x q[4];
rz(1.8795368) q[6];
cx q[12],q[15];
cx q[13],q[9];
id q[2];
x q[3];
cx q[10],q[0];
cx q[7],q[11];
cx q[8],q[5];
id q[14];
id q[5];
sx q[13];
cx q[12],q[0];
cx q[1],q[4];
cx q[15],q[6];
rz(4.1763805) q[10];
cx q[8],q[9];
id q[14];
cx q[3],q[2];
cx q[11],q[7];
rz(4.0459119) q[1];
cx q[11],q[10];
x q[4];
id q[3];
rz(5.3085798) q[9];
cx q[12],q[6];
sx q[7];
x q[15];
cx q[5],q[14];
x q[2];
cx q[0],q[8];
id q[13];
sx q[0];
cx q[5],q[10];
rz(1.3935683) q[14];
cx q[11],q[9];
rz(2.83925) q[8];
id q[13];
cx q[4],q[15];
cx q[2],q[1];
sx q[3];
x q[7];
sx q[6];
rz(4.9129787) q[12];
id q[9];
rz(0.55948103) q[10];
cx q[0],q[8];
id q[3];
id q[12];
cx q[7],q[2];
id q[15];
rz(3.8476134) q[6];
cx q[11],q[5];
cx q[1],q[14];
x q[4];
x q[13];
cx q[6],q[0];
cx q[5],q[9];
id q[4];
sx q[1];
rz(5.4876479) q[3];
x q[7];
rz(2.2632154) q[14];
cx q[10],q[2];
cx q[15],q[13];
rz(2.2378222) q[12];
sx q[11];
x q[8];
id q[4];
cx q[3],q[5];
rz(0.82937556) q[7];
cx q[8],q[2];
cx q[10],q[12];
cx q[1],q[9];
rz(5.2608423) q[6];
rz(0.83401574) q[15];
rz(6.030243) q[11];
cx q[14],q[0];
x q[13];
cx q[9],q[12];
rz(2.5671638) q[15];
id q[14];
cx q[10],q[8];
x q[11];
cx q[0],q[2];
x q[1];
cx q[7],q[5];
rz(1.372442) q[3];
x q[13];
id q[4];
id q[6];
cx q[6],q[15];
cx q[12],q[11];
cx q[14],q[3];
x q[13];
sx q[1];
cx q[0],q[4];
cx q[2],q[10];
id q[8];
cx q[9],q[5];
sx q[7];
id q[12];
cx q[9],q[1];
cx q[13],q[6];
rz(0.21164192) q[10];
cx q[0],q[11];
cx q[15],q[3];
cx q[14],q[4];
cx q[2],q[5];
x q[8];
x q[7];
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
measure q[4] -> c[4];
measure q[5] -> c[5];
measure q[6] -> c[6];
measure q[7] -> c[7];
measure q[8] -> c[8];
measure q[9] -> c[9];
measure q[10] -> c[10];
measure q[11] -> c[11];
measure q[12] -> c[12];
measure q[13] -> c[13];
measure q[14] -> c[14];
measure q[15] -> c[15];