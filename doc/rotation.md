# Rotation physics

## Rodrigues formula

$$
\mathbf{p}_{rot} = 
 \cos \theta \mathbf{p}+ \sin \theta  (\mathbf{r} \cdot \mathbf{p})\mathbf{r} + (1 - \cos \theta)(\mathbf{r} \times \mathbf{p}) 
$$
where, $\mathbf{r}$ is rotation axis, $\mathbf{p}$ is point, and $\theta$ is rotation angle.

**Matrix**
$$
\mathbf{R} =\begin{bmatrix}
 \cos \theta + r_x^2(1 - \cos \theta) & r_x r_y (1 - \cos \theta) - r_z \sin \theta & r_x r_z (1 - \cos \theta) + r_y \sin \theta \\
r_y r_x (1 - \cos \theta) + r_z \sin \theta & \cos \theta + r_y^2(1 - \cos \theta) & r_y r_z (1 - \cos \theta) - r_x \sin \theta \\
r_z r_x (1 - \cos \theta) - r_y \sin \theta & r_z r_y (1 - \cos \theta) + r_x \sin \theta & \cos \theta + r_z^2(1 - \cos \theta)
\end{bmatrix}
$$

-----------------------------
## Quaternions
$$
\begin{align*}
\mathbf{q} &= w + x i + yj + zk \\
& = (w, \mathbf{v})
\end{align*}
$$

### Vector rotation
Rotation of angle $\theta$ around axis $\mathbf{r}$,
$$
\mathbf{q} = (\cos \frac{\theta}{2}, \sin \frac{\theta}{2} \mathbf{r})
$$
Rotation of vector $\mathbf{p}$,
$$
\mathbf{p}_{rot} = \mathbf{q}\mathbf{p}\mathbf{q}^{-1}
$$


### In matrix form
A unit rotaion quaternion $\mathbf{q}$ can be represented as,
$$
\mathbf{R_q} = \begin{bmatrix}
1 - 2y^2 - 2z^2 & 2xy - 2zw & 2xz + 2yw \\
2xy + 2zw & 1 - 2x^2 - 2z^2 & 2yz - 2xw \\
2xz - 2yw & 2yz + 2xw & 1 - 2x^2 - 2y^2
\end{bmatrix}
$$

