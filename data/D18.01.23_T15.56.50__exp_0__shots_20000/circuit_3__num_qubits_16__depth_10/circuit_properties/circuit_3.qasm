OPENQASM 2.0;
include "qelib1.inc";
qreg q[16];
creg c[16];
cx q[11],q[7];
sx q[13];
rz(2.0154396) q[4];
id q[9];
cx q[14],q[1];
rz(5.229277) q[3];
cx q[12],q[10];
cx q[8],q[6];
rz(1.0888443) q[2];
cx q[0],q[5];
x q[15];
cx q[1],q[9];
cx q[7],q[4];
sx q[11];
rz(6.2024724) q[12];
cx q[2],q[5];
cx q[3],q[0];
cx q[15],q[8];
cx q[6],q[13];
cx q[14],q[10];
sx q[9];
cx q[12],q[6];
cx q[5],q[13];
cx q[8],q[7];
id q[14];
cx q[11],q[0];
cx q[10],q[1];
x q[4];
cx q[3],q[15];
x q[2];
sx q[14];
cx q[9],q[8];
x q[12];
x q[13];
sx q[0];
id q[15];
cx q[5],q[4];
id q[3];
rz(6.2068829) q[11];
cx q[7],q[2];
cx q[10],q[1];
id q[6];
rz(1.8944531) q[8];
x q[13];
cx q[1],q[9];
x q[12];
cx q[2],q[14];
x q[4];
cx q[6],q[7];
cx q[10],q[15];
x q[0];
rz(1.0773994) q[3];
id q[5];
id q[11];
cx q[12],q[14];
cx q[0],q[8];
rz(1.9163592) q[7];
id q[9];
cx q[3],q[5];
x q[10];
x q[13];
id q[1];
cx q[15],q[6];
sx q[4];
cx q[2],q[11];
id q[1];
cx q[15],q[3];
id q[7];
cx q[14],q[6];
cx q[11],q[12];
id q[0];
cx q[10],q[8];
rz(5.475918) q[4];
sx q[2];
cx q[13],q[9];
x q[5];
id q[4];
cx q[14],q[1];
id q[10];
sx q[0];
sx q[2];
cx q[13],q[12];
id q[11];
rz(1.6854656) q[5];
sx q[8];
cx q[3],q[6];
cx q[9],q[7];
sx q[15];
sx q[6];
cx q[14],q[5];
sx q[8];
x q[15];
x q[9];
cx q[2],q[1];
rz(1.5657998) q[12];
x q[4];
rz(2.7961159) q[3];
x q[7];
cx q[0],q[11];
cx q[10],q[13];
cx q[5],q[7];
cx q[0],q[15];
rz(1.0540291) q[6];
cx q[10],q[12];
sx q[14];
cx q[4],q[3];
sx q[2];
sx q[1];
cx q[13],q[8];
sx q[11];
sx q[9];
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
