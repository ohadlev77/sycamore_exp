OPENQASM 2.0;
include "qelib1.inc";
qreg q[12];
creg c[12];
cx q[5],q[2];
cx q[1],q[11];
x q[0];
cx q[7],q[10];
rz(0.95753871) q[8];
id q[3];
sx q[6];
cx q[9],q[4];
cx q[7],q[9];
cx q[3],q[11];
x q[4];
rz(5.9011925) q[5];
sx q[0];
sx q[8];
id q[10];
sx q[6];
cx q[2],q[1];
cx q[10],q[8];
cx q[3],q[5];
rz(3.2171634) q[4];
id q[9];
cx q[6],q[2];
cx q[7],q[0];
x q[11];
id q[1];
rz(5.064579) q[5];
x q[10];
cx q[1],q[7];
sx q[9];
cx q[3],q[6];
cx q[0],q[8];
cx q[2],q[4];
rz(2.7201254) q[11];
cx q[10],q[5];
id q[7];
id q[2];
cx q[9],q[4];
sx q[3];
x q[6];
cx q[1],q[8];
x q[0];
id q[11];
rz(4.0009474) q[8];
sx q[1];
rz(1.7090693) q[5];
cx q[9],q[11];
sx q[0];
cx q[10],q[3];
sx q[2];
cx q[4],q[6];
sx q[7];
id q[10];
cx q[2],q[6];
id q[11];
rz(0.37140559) q[5];
cx q[1],q[8];
id q[4];
id q[7];
cx q[0],q[3];
x q[9];
x q[5];
x q[11];
cx q[0],q[2];
rz(3.3518719) q[1];
rz(3.4997108) q[3];
x q[6];
x q[7];
rz(3.5454584) q[8];
cx q[4],q[10];
x q[9];
cx q[11],q[7];
cx q[5],q[0];
cx q[6],q[8];
id q[2];
cx q[10],q[3];
rz(1.3418796) q[9];
id q[4];
rz(6.0494013) q[1];
x q[8];
cx q[3],q[4];
cx q[2],q[0];
x q[7];
cx q[1],q[10];
sx q[9];
cx q[11],q[5];
x q[6];
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
