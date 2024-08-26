
    def main(self, P, B, K, ASC, O, D, JI, JO, fBay):

        ##################### ***************** #######################
        POPL = self.init_population(P, P['iVar'])   # 初始序列的
        POPL, Elite, OUTD = self.fitness(ASC, B, K, O, D, JI, JO, fBay, POPL)

        time_1 = time.time()
        PM1 = {'PC1': 0, 'PC2': 0, 'PM1': 0, 'PM2': 0, 'PM3': 0, 'PM4': 0}

        idx_c1, idx_c2, idx_m1, idx_m2, idx_m3, idx_m4 = 0, 0, 0, 0, 0, 0
        v_objective = list()
        Pro_best = {}
        Pro_cur = {}

        for g in range(P['iGen']):
            ###########################  crossover  ############################
            rpc = random.randint(1, 2)
            if rpc == 1:
                POPL = self.crossover_Single(P, POPL)
                idx_c1 += 1
            elif rpc == 2:
                POPL = self.crossover_Multiple(P, POPL)
                idx_c2 += 1

            ###########################   mutation  ############################
            # POPL = self.mutate_Exchange(P, POPL, JI, JO)
            # POPL = self.mutate_Insert(P, POPL, JI, JO)
            # POPL = self.mutate_2Opt(P, POPL)

            rpm = random.randint(1, 3)
            if rpm == 1:
                POPL = self.mutate_Exchange(P, POPL, JI, JO)
                idx_m1 += 1
            elif rpm == 2:
                POPL = self.mutate_Insert(P, POPL, JI, JO)
                idx_m2 += 1
            elif rpm == 3:
                POPL = self.mutate_2Opt(P, POPL)
                idx_m3 += 1
            # else:
            #     POPL = self.mutate_Reverse(P, POPL)
            #     idx_m4 += 1
            ip = 1
            POPL, Elitec, OUTD = self.fitness(ASC, B, K, O, D, JI, JO, fBay, POPL)
            A = []
            for i in range(len(POPL)):
                A.append(POPL[i]['fitness'])

            # POP, Elitec = flexibleSchedulingASC.assignMent_sequential(P, POP)
            if Elitec['fitness'] < Elite['fitness']:
                # print(g, rpc, rpm, Elitec['fitness'], Elite['fitness'])
                Pro_best[g] = Elitec['fitness']

                if rpc == 1: PM1['PC1'] += 1
                if rpc == 2: PM1['PC2'] += 1
                if rpm == 1: PM1['PM1'] += 1
                if rpm == 2: PM1['PM2'] += 1
                if rpm == 3: PM1['PM3'] += 1
                if rpm == 4: PM1['PM4'] += 1

                Elite = Elitec.copy()
            else:
                Pro_best[g] = Elite['fitness']

            # Pro_cur[g] = Elitec['fitness']
            Pro_cur[g] = np.average([np.min(A), Pro_best[g]])
            # Pro_cur[g] = np.min(A)
            v_objective.append(Elite['Obj'])
        # print('v_objective =', v_objective)
        # print('finnal elite: ', 'decoded =', Elite['decoded'])
        # print('final objective: ', v_objective[-1])
        fmakespan = v_objective[-1]

        PM2 = {'PC1': idx_c1, 'PC2': idx_c2, 'PM1': idx_m1, 'PM2': idx_m2, 'PM3': idx_m3, 'PM4': idx_m4}
        cpu = np.round(time.time() - time_1, 4)

        return OUTD, fmakespan, cpu, PM1, PM2, Pro_best, Pro_cur

    def init_population(self, P, N):
        POPL = []
        for i in range(1, P['iPop']+1):
            x = random.sample(range(1, N + 1), N)
            POPL.append({'x': x, 'decoded': list(), 'Obj': np.inf, 'fitness': np.inf})
        return POPL

    def crossover_Single(self, P, POPL):
        for i in range(P['iPop']):
            if random.random() <= P['x_over']:
                continue
            randS = random.sample(range(P['iPop']), 2)
            # print('crossing')

            is1, is2 = randS[0], randS[1]
            sequence1 = POPL[is1]['x']
            sequence2 = POPL[is2]['x']

            idx1 = random.randint(0, len(sequence1) - 1)
            idx2 = random.randint(0, len(sequence2) - 1)
            temp_it1 = sequence1.copy()[idx1]
            temp_it2 = sequence2.copy()[idx2]

            sequence1[idx1] = temp_it2
            sequence2[idx2] = temp_it1
            mul_idx1 = [i for i, val in enumerate(sequence1) if val == sequence1[idx1]]
            mul_idx2 = [i for i, val in enumerate(sequence2) if val == sequence2[idx2]]
            if len(mul_idx1) >= 2 and len(mul_idx2) >= 2:
                idx_1_1 = list(set(mul_idx1) - set([idx1]))
                idx_2_1 = list(set(mul_idx2) - set([idx2]))
                sequence1[idx_1_1[0]] = temp_it1
                sequence2[idx_2_1[0]] = temp_it2

            POPL[is1]['x'] = sequence1
            POPL[is2]['x'] = sequence2

        return POPL

    def crossover_Multiple(self, P, POPL):
        for i in range(P['iPop']):
            if random.random() <= P['x_over']:
                continue
            randS = random.sample(range(P['iPop']), 2)
            # print('crossing')

            is1, is2 = randS[0], randS[1]
            sequence1 = POPL[is1]['x']
            sequence2 = POPL[is2]['x']
            # print(POPL)
            # print('#', sequence1, sequence2)

            idx1 = random.randint(1, len(sequence1) - 3)
            idx2 = random.randint(1, len(sequence2) - 3)
            sequence1_C = copy.deepcopy(sequence1)
            sequence2_C = copy.deepcopy(sequence2)
            it1a, it1b = sequence1_C[idx1], sequence1_C[idx1+1] # 要交叉的连续任务 2,6
            it2a, it2b = sequence2_C[idx2], sequence2_C[idx2+1] # 要交叉的连续任务 3,4
            idx1_a, idx1_b = sequence1_C.index(it2a), sequence1_C.index(it2b) # idx(3) idx(4)
            idx2_a, idx2_b = sequence2_C.index(it1a), sequence2_C.index(it1b) # idx(2) idx(6)

            temp_it1_a = sequence1_C[:idx1]
            temp_it1_b = sequence1_C[idx1: idx1+2]
            temp_it1_c = sequence1_C[idx1+2:]
            temp_it2_a = sequence2_C[:idx2]
            temp_it2_b = sequence2_C[idx2: idx2+2]
            temp_it2_c = sequence2_C[idx2+2:]
            sequence1 = temp_it1_a + temp_it2_b + temp_it1_c    # 包含重复元素的新解
            sequence2 = temp_it2_a + temp_it1_b + temp_it2_c    # 包含重复元素的新解

            ## 处理冲突
            if it1a not in sequence1:
                sequence1[idx1_a] = it1a
            if it1b not in sequence1:
                sequence1[idx1_b] = it1b
            if it2a not in sequence2:
                sequence2[idx2_a] = it2a
            if it2b not in sequence2:
                sequence2[idx2_b] = it2b


            POPL[is1]['x'] = sequence1
            POPL[is2]['x'] = sequence2

        return POPL

    def mutate_2Opt(self, P, POPL):    # 2-opt
        for i in range(len(POPL)):
            sequence = POPL[i]['x']
            if random.random() <= float(P['mut']):
                rand_a = random.randint(1, int(np.floor(0.5 * len(sequence))))
                rand_b = random.randint(int(np.ceil(0.5 * len(sequence))) + 1, len(sequence) - 2)
                node_a = sequence[:rand_a]
                node_b = sequence[rand_a:rand_b]
                node_b = node_b[::-1]
                node_c = sequence[rand_b:]
                sequence = node_a + node_b + node_c
                POPL[i]['x'] = sequence

        return POPL

    def mutate_Exchange(self, P, POPL, JI, JO):     # exchange
        for i in range(len(POPL)):
            sequence = POPL[i]['x']
            if random.random() <= float(P['mut']): #1
                X = self.continuousJuiceThree(JI, JO, sequence)
                if X != False:
                    temp_1 = sequence[int(X[0])]
                    temp_2 = sequence[int(X[1])]
                    sequence[X[1]] = temp_1
                    sequence[X[0]] = temp_2
                    POPL[i]['x'] = sequence
        return POPL

    def mutate_Insert(self, P, POPL, JI, JO):  # insert
        for i in range(len(POPL)):
            sequence = POPL[i]['x']
            if random.random() <= float(P['mut']):
                X = self.continuousJuiceTwo(JI, JO, sequence)
                if X != False:
                    if X[0] < X[1]: # 待插入任务 位于 插入点之前
                        sequence.insert(X[1], sequence[X[0]])
                        sequence.remove(sequence[X[0]])
                    if X[0] > X[1]: # 待插入任务 位于 插入点之后
                        sequence.insert(X[1], sequence[X[0]])
                        sequence.pop(X[0] + 1)
                POPL[i]['x'] = sequence

        return POPL

    def mutate_Reverse(self, P, POPL):   ## reverse
        # print("Operator: intraRoute_Reverse...")
        POP_R = copy.deepcopy(POPL)
        for i in range(len(POP_R)):
            sequence = POP_R[i]['x']
            if random.random() <= float(P['mut']):
                sequence.reverse()
                POPL[i]['x'] = sequence
        return POPL

    def continuousJuiceThree(self, JI, JO, sequence):
        X_in, X_out = [], []        # 进出口箱子的索引
        idx3_IN, idx3_OUT = [], []    # 任务类型连续3次的索引
        idx2_IN, idx2_OUT = [], []    # 任务类型连续2次的索引

        for i in sequence:
            if i in JI:
                X_in.append(sequence.index(i))
            if i in JO:
                X_out.append(sequence.index(i))

        for idx in range(len(X_in) - 2):    # 索引
            if X_in[idx + 1] - X_in[idx] == 1:
                idx2_IN.append(idx)         ## 2
                if X_in[idx + 2] - X_in[idx] == 2:
                    idx3_IN.append(idx)     ## 3
            if len(idx3_IN) == 0:  # 如果3为空, 则向降序方向搜索
                if X_in[idx] - X_in[idx + 1] == 1 and X_in[idx] - X_in[idx + 2] == 2: # 降序3
                    idx3_IN.append(idx)
            if len(idx2_IN) == 0:  # 如果2为空, 则向降序方向搜索
                if X_in[idx] - X_in[idx + 1] == 1: # 降序2
                    idx2_IN.append(idx)

            if len(idx3_IN) != 0 and len(idx2_IN) != 0:
                break

        for idx in range(len(X_out) - 2):  # 索引
            if X_out[idx + 1] - X_out[idx] == 1:
                idx2_OUT.append(idx)  ## 2
                if X_out[idx + 2] - X_out[idx] == 2:
                    idx3_OUT.append(idx)  ## 3
            if len(idx3_OUT) == 0:  # 如果3为空, 则向降序方向搜索
                if X_out[idx] - X_out[idx + 1] == 1 and X_out[idx] - X_out[idx + 2] == 2:  # 降序3
                    idx3_OUT.append(idx)
            if len(idx2_OUT) == 0:  # 如果2为空, 则向降序方向搜索
                if X_out[idx] - X_out[idx + 1] == 1:  # 降序2
                    idx2_OUT.append(idx)
            if len(idx3_OUT) != 0 and len(idx2_OUT) != 0:
                break


        if len(idx3_IN) != 0:       # 连续3个进口箱
            if len(idx3_OUT) != 0:  # 连续3个出口箱
                return [X_in[idx3_IN[0] + 1], X_out[idx3_OUT[0] + 1]]      # 这两个就exchange喽
            # elif len(idx2_OUT) != 0:# 连续2个出口箱
            #     return [X_in[idx3_IN[0] + 1], X_out[idx2_OUT[0] + 1]]    # 这两个就exchange喽
            else:
                return False

        # elif len(idx2_IN) != 0:     # 连续2个进口箱
        #     if len(idx3_OUT) != 0:  # 连续3个出口箱
        #         return [X_in[idx2_IN[0] + 1], X_out[idx3_OUT[0] + 1]]     # 这两个就exchange喽
        #     elif len(idx2_OUT) != 0:  # 连续2个出口箱
        #         return [X_in[idx2_IN[0] + 1], X_out[idx2_OUT[0] + 1]]  # 这两个就exchange喽
        #     else:
        #         return False
        else:
            return False

    def continuousJuiceTwo(self, JI, JO, sequence):
        it = random.randint(1, len(sequence))
        idx_it = sequence.index(it)

        X_in, X_out = [], []  # 进出口箱子的索引
        idx2_IN, idx2_OUT = [], []  # 任务类型连续2次的索引

        if it in JO:        ### JI 插入到两个相邻的JO中间
            for i in sequence:
                if i in JI:
                    X_in.append(sequence.index(i))

            for idx in range(len(X_in) - 2):    # 索引
                if X_in[idx + 1] - X_in[idx] == 1:
                    idx2_IN.append(idx)         ## 2
                if len(idx2_IN) == 0:           # 如果2为空, 则向降序方向搜索
                    if X_in[idx] - X_in[idx + 1] == 1:  # 降序2
                        idx2_IN.append(idx)
                if len(idx2_IN) != 0:
                    break

            if len(idx2_IN) != 0:       # 连续2个进口箱
                return [idx_it, X_in[idx2_IN[0] + 1]]   # sequence中位置idx_it的任务，插入到位置X_in[idx2_IN[0]]中
            else:
                return False

        if it in JI:
            for idx in range(len(X_out) - 2):  # 索引
                if X_out[idx + 1] - X_out[idx] == 1:
                    idx2_OUT.append(idx)  ## 2
                if len(idx2_OUT) == 0:  # 如果2为空, 则向降序方向搜索
                    if X_out[idx] - X_out[idx + 1] == 1:  # 降序2
                        idx2_OUT.append(idx)
                if len(idx2_OUT) != 0:
                    break
            if len(idx2_OUT) != 0:       # 连续2个进口箱
                return [idx_it, X_out[idx2_OUT[0] + 1]]   # sequence中位置idx_it的任务，插入到位置X_out[idx2_IN[0]]中
            else:
                return False






