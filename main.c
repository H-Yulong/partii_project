#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

// The factorial function, containing pre-computed values for acceration.
int fact(int n){
    switch (n){
    	case 0:
    		return 1;
    		break;
    	case 1:
    		return 1;
    		break;
    	case 2:
    		return 2;
    		break;
    	case 3:
    		return 6;
    		break;
    	case 4:
    		return 24;
    		break;
    	case 5:
    		return 120;
    		break;
    	default:
    		return n * fact(n-1);
    }
}

// Calculates the probability of getting a given roll
double prRoll(int* arr){
    //Initialize count
    int count[6];
    for (int i=0; i<6; i++){
    	count[i] = 0;
    }

    //ASSERT: arr would have size 5, and values from {1,2,3,4,5,6}.
    for (int i=0; i<5; i++){
        count[arr[i]-1] = count[arr[i]-1] + 1;
    }

    // 5/324 = (5!)/(6^5), for simplicity
    double result = 5.0 / 324;

    for (int i=0; i<6; i++){
    	result = result / fact(count[i]);
    }

    return result;
}

// Generates all the possible dice-roll patterns for n dice with d faces (default 6)
// Returning a list of lists
int** dicePatterns(int n){
	//ASSERT: n is in [0,5], temp stores the number of items we need to generate.
    int d = 6, p = 0, buffer[n], terminate[n], rp = 0, temp[] = {1,6,21,56,126,252};
    int** result = calloc(temp[n],sizeof(int*));
    if(n == 0){
    	result[0] = calloc(1,sizeof(int));
    	return result;
    }

    for (int i=0; i<n; i++){
    	buffer[i] = 1;
    	terminate[i] = d;
    }

    while (memcmp(buffer, terminate, n*sizeof(int)) != 0){
    	result[rp] = malloc(n*sizeof(int));
    	for (int j=0; j<n; j++){
			result[rp][j] = buffer[j];
		}
		rp++;

		if (buffer[p] == d){
			while (buffer[p] == d){
				p++;
			}
			buffer[p] = buffer[p] + 1;
			while (p != 0){
				p--;
				buffer[p] = buffer[p + 1];
			}
		}else{
			buffer[p]++;
		}
    }

    result[rp] = malloc(n*sizeof(int));
	for (int j=0; j<n; j++){
		result[rp][j] = terminate[j];
	}

    return result;
}

// This is OBVIOUS
int contains(int* arr, int e, int size){
	for (int i=0; i<size; i++){
		if (arr[i] == e){
			return i;
		}
	}
	return -1;
}

// Generates all possible outcomes of choosing r numbers from [0,1,2...13]
// Order doesn't matter
int** choosePatterns(int r){
	//ASSERT: r is in range [1,12].
	int p = 0, n = 13, buffer[r], terminate[r], rp=0, temp[] = {1,14,90,352,935,1782,2508,2640,2079,1210,506,144,25};
    int** result = calloc(temp[r],sizeof(int*));

    for (int i=0; i<r; i++){
    	buffer[i] = r - i - 1;
    	terminate[i] = 13 - i - 1;
    }

    while(memcmp(buffer, terminate, r*sizeof(int)) != 0){
    	int pos = contains(buffer,0,r);
    	if (pos >= 0){
    		result[rp] = malloc(r*sizeof(int));
	    	for (int j=0; j<r; j++){
	    		if (j == pos){
	    			result[rp][j] = -1;
	    		}else{
	    			result[rp][j] = buffer[j];
	    		}
			}
			rp++;
    	}

    	result[rp] = malloc(r*sizeof(int));
    	for (int j=0; j<r; j++){
			result[rp][j] = buffer[j];
		}
		rp++;

		if (buffer[p] == 12){
			while (buffer[p] + p == 12){
				p++;
			}
			buffer[p] = buffer[p] + 1;
			while (p != 0){
				p = p - 1;
                buffer[p] = buffer[p + 1] + 1;
			}
		}else{
			buffer[p] = buffer[p] + 1;
		}

    }

    result[rp] = malloc(r*sizeof(int));
	for (int j=0; j<r; j++){
		result[rp][j] = terminate[j];
	}

    return result;
}

// A bunch of yahtzee category functions.
// ASSERT: dice is an array of size 5, up is in range [0,63].
int yahtzee(int* dice, int up){
    if ((dice[0] == dice[1]) && (dice[0] == dice[2]) && (dice[0] == dice[3]) && (dice[0] == dice[4])){
        return 50;
    }
    else{
        return 0;
    }
}

int ones(int* dice, int up){
    int count = 0;
    for(int i=0; i<5; i++){
    	if (dice[i] == 1){
    		count++;
    	}
    }

    if ((up != 63) && (count + up >= 63)){
        return count + 35;
    }
    else{
        return count;
    }
}

int twos(int* dice, int up){
    int count = 0;
    for(int i=0; i<5; i++){
    	if (dice[i] == 2){
    		count += 2;
    	}
    }

    if ((up != 63) && (count + up >= 63)){
        return count + 35;
    }
    else{
        return count;
    }
}

int threes(int* dice, int up){
    int count = 0;
    for(int i=0; i<5; i++){
    	if (dice[i] == 3){
    		count += 3;
    	}
    }

    if ((up != 63) && (count + up >= 63)){
        return count + 35;
    }
    else{
        return count;
    }
}

int fours(int* dice, int up){
    int count = 0;
    for(int i=0; i<5; i++){
    	if (dice[i] == 4){
    		count += 4;
    	}
    }

    if ((up != 63) && (count + up >= 63)){
        return count + 35;
    }
    else{
        return count;
    }
}

int fives(int* dice, int up){
    int count = 0;
    for(int i=0; i<5; i++){
    	if (dice[i] == 5){
    		count += 5;
    	}
    }

    if ((up != 63) && (count + up >= 63)){
        return count + 35;
    }
    else{
        return count;
    }
}

int sixes(int* dice, int up){
    int count = 0;
    for(int i=0; i<5; i++){
    	if (dice[i] == 6){
    		count += 6;
    	}
    }

    if ((up != 63) && (count + up >= 63)){
        return count + 35;
    }
    else{
        return count;
    }
}

int sum(int* dice){
	int result = 0;
	for(int i=0; i<5; i++){
		result += dice[i];
	}
	return result;
}

int three_of_a_kind(int* dice, int up){
    int count[] = {0, 0, 0, 0, 0, 0};
    for(int i=0; i<5; i++){
    	count[dice[i] - 1]++;
    }
    for(int i=0; i<6; i++){
    	if (count[i] >= 3){
    		return sum(dice);
    	}
    }
    return 0;
}

int four_of_a_kind(int* dice, int up){
    int count[] = {0, 0, 0, 0, 0, 0};
    for(int i=0; i<5; i++){
    	count[dice[i] - 1]++;
    }
    for(int i=0; i<6; i++){
    	if (count[i] >= 4){
    		return sum(dice);
    	}
    }
    return 0;
}

int fullhouse(int* dice, int up){
    int count[] = {0, 0, 0, 0, 0, 0};
    for(int i=0; i<5; i++){
    	count[dice[i] - 1]++;
    }
    if ((contains(count,2,6) >= 0) && (contains(count,3,6) >= 0)){
        return 25;
    }
    else{
        return 0;
    }
}

int small_straight(int* dice, int up){
    if ((contains(dice,1,5) >= 0) && (contains(dice,2,5) >= 0) && (contains(dice,3,5) >= 0) && (contains(dice,4,5) >= 0)){
        return 30;
    }
    else if ((contains(dice,2,5) >= 0) && (contains(dice,3,5) >= 0) && (contains(dice,4,5) >= 0) && (contains(dice,5,5) >= 0)){
        return 30;
    }
    else if ((contains(dice,3,5) >= 0) && (contains(dice,4,5) >= 0) && (contains(dice,5,5) >= 0) && (contains(dice,6,5) >= 0)){
        return 30;
    }
    else{
        return 0;
    }
}

int large_straight(int* dice, int up){
    if ((contains(dice,1,5) >= 0) && (contains(dice,2,5) >= 0) && (contains(dice,3,5) >= 0) && (contains(dice,4,5) >= 0) && (contains(dice,5,5) >= 0)){
        return 40;
    }
    else if ((contains(dice,2,5) >= 0) && (contains(dice,3,5) >= 0) && (contains(dice,4,5) >= 0) && (contains(dice,5,5) >= 0) && (contains(dice,6,5) >= 0)){
        return 40;
    }else{
        return 0;
    }
}

int chance(int* dice, int up){
    return sum(dice);
}

// Code a score state uniquely.
// -1 represents the state with all categories filled.
int code(int* cats, int up, int size){
    // ASSERT: size is the size of array that cats points to.
    if (size == 13){
        return -1;
    }
    
    int result = 0;
    for(int i=0; i<size; i++){
        result += pow(2, cats[i]+1);
    }
    result = result * 64 + up;
    return result;
}

int* append(int* cats, int c, int size){
	int* result = malloc(sizeof(int)*(size+1));
	for (int i=0; i<size; i++){
		result[i] = cats[i];
	}
	result[size] = c;
	return result;
}

double evaluate(int* dice, int cat, int up, int* cats, int cats_size, double* dictionary){
	// ASSERT: size is the cats_size of array that cats points to.
	// ASSERT: problematic parameters won't be used. If you see "Segmentation Fault", that's probably your fault.

    // Initialization
    int score = 0;

    // First evaluation
    switch (cat){
    	case 0:
    		score = yahtzee(dice, up);
    		break;
    	case 1:
    		score = ones(dice, up);
    		break;
    	case 2:
    		score = twos(dice, up);
    		break;
    	case 3:
    		score = threes(dice, up);
    		break;
    	case 4:
    		score = fours(dice, up);
    		break;
    	case 5:
    		score = fives(dice, up);
    		break;
    	case 6:
    		score = sixes(dice, up);
    		break;
    	case 7:
    		score = three_of_a_kind(dice, up);
    		break;
    	case 8:
    		score = four_of_a_kind(dice, up);
    		break;
    	case 9:
    		score = fullhouse(dice, up);
    		break;
    	case 10:
    		score = small_straight(dice, up);
    		break;
    	case 11:
    		score = large_straight(dice, up);
    		break;
    	case 12:
    		score = chance(dice, up);
    		break;
    	default:
    		return -1.0;
    }

    if ((cat == 0) && (score == 0)){
        cat = -1;
    }

    // Handle upper bonus counter
    if ((cat < 7) && (cat > 0) && (up < 63)){
        up = up + score;
        if (up > 63) {
            up = 63;
        }
     }

    // Joker rule and Yahtzee bonus
    if ((contains(cats, 0, cats_size) >= 0) && (yahtzee(dice, up) > 0)){
        if (dice[0] == cat){
            score += 100;
        }else if (contains(cats, dice[0], cats_size) < 0){
            return 0;
        }else{
            score += 100;
            if (cat == 9){
                score += 25;
            }else if (cat == 10){
                score += 30;
            }else if (cat == 11){
                score += 40;
            }
        }
    }

    int* new_cats = append(cats, cats_size, cat);
    //score += dictionary[code(new_cats, up, cats_size+1)];
    free(new_cats);
    return score;
}

// Adds d in array dice, preserving the order.
int* extendDice(int* dice, int d, int size){
	// ASSERT: size is the size of array that dice points to.
	int* result = malloc(sizeof(int)*(size+1));
	int pos = -1, i = 0;
	while (pos < 0){
		if (i == 0){
			if (d >= dice[0]){
				pos = 0;
			}
		}else if(i == size){
			pos = size;
		}else{
			if( (dice[i-1] >= d) && (dice[i] <= d)){
				pos = i;
			}
		}
		i++;
	}

	for(int j=0; j<=size; j++){
		if(j < pos){
			result[j] = dice[j];
		}else if(j == pos){
			result[j] = d; 
		}else{
			result[j] = dice[j-1];
		}
	}

	return result;
}

// Removes d in array dice, preserving the order.
int* removeDice(int* dice, int d, int size){
	// ASSERT: size is the size of array that dice points to.
    int temp = contains(dice, d, size);
    if(temp >= 0){
    	int* result = malloc(sizeof(int)*(size - 1));
    	for(int i=0; i<size; i++){
    		if(i < temp){
    			result[i] = dice[i];
    		}else if(i > temp){
    			result[i-1] = dice[i];
    		}
    	}
        return result;
    }
    return NULL;
}

int find(int** lib, int* row, int row_size, int entries){
	for (int i=0; i<entries; i++){
		int found = 0;
		for(int j=0; j<row_size; j++){
			if (row[j] == lib[i][j]){
				found++;
			}
		}

		if (found == row_size){
			return i;
		}
	}
	return -1;
}

double expectation(int*** cache, int* empty, int up, int* cats, int cats_size, double* dictionary){
	int cache_sizes[] = {1,6,21,56,126,252};
	int cache_indexes[] = {0,1,7,28,84,210};
    double R3[252];
    // Evaluate R3
    for(int i=0; i<252; i++){
    	int* d = cache[5][i];
    	double max_exp = 0.0;

    	for(int j=0; j<(13 - cats_size); j++){
    		double score = evaluate(d, empty[j], up, cats, cats_size, dictionary);
    		if (score > max_exp){
    			max_exp = score;
    		}
    	}
    	R3[i] = max_exp;
    }

    // Evaluate K2
    double K2[462];
    for (int i=0; i<252; i++){
    	K2[210+i] = R3[i];
    }
    for (int k=4; k>=0; k = k-1){
    	for (int i=0; i<cache_sizes[k]; i++){
    		double exp = 0;
    		for (int e=1; e<7; e++){
    			int* new_d = extendDice(cache[k][i],e,k);
    			//printf("%f\n",K2[cache_indexes[k+1] + find(cache[k+1], new_d, k, cache_sizes[k+1])]);
    			exp += K2[cache_indexes[k+1] + find(cache[k+1], new_d, k+1, cache_sizes[k+1])];
    		}
    		K2[cache_indexes[k]+i] = exp / 6.0;
    	}
    }
	
    




        /*
for(int i=0; i<462; i++){
    	printf("%d %f\n",i,K2[i]);
    }
    # Evaluate R2
    R2 = {0: K2.get(0)}
    for k in range(1, 6):
        for d in cache[k]:
            max_exp = K2.get(cache[k].index(d) * 10 + k)
            for e in range(1, 7):
                r = remove(d, e)
                if r or (r == []):
                    max_exp = max(max_exp, R2[cache[k - 1].index(r) * 10 + k - 1])
            R2[cache[k].index(d) * 10 + k] = max_exp

    # Evaluate K1
    K1 = {}
    for d in cache[5]:
        K1[cache[5].index(d) * 10 + 5] = R2[cache[5].index(d) * 10 + 5]
    for k in range(4, -1, -1):
        for d in cache[k]:
            exp = 0
            for e in range(1, 7):
                new_d = extend(d, e)
                exp += K1[cache[k + 1].index(new_d) * 10 + k + 1]
            K1[cache[k].index(d) * 10 + k] = exp / 6


    # Evaluate R1
    R1 = {0: K1.get(0)}
    for k in range(1, 6):
        for d in cache[k]:
            max_exp = K1.get(cache[k].index(d) * 10 + k)
            for e in range(1, 7):
                r = remove(d, e)
                if r or (r == []):
                    max_exp = max(max_exp, R1[cache[k - 1].index(r) * 10 + k - 1])
            R1[cache[k].index(d) * 10 + k] = max_exp

    # Evaluate expectation
    exp = 0
    for key, val in R1.items():
        if key % 10 == 5:
            exp += prRoll(cache[5][key // 10]) * val

    return exp
    */
}

int main(){
	int** cache[6];
	for(int i=0; i<6; i++){
		cache[i] = dicePatterns(i);
	}
	int empty[] = {12};
	int d[] = {6,6,5};
	int* s = extendDice(d, 6, 3);
	int cats[] = {11,10,9,8,7,6,5,4,3,2,1,-1};
	double* dict;
	//printf("%d\n",find(cache[4], s, 4, 126));
	expectation(cache, empty, 12, cats, 12, dict);
	return 0;
}

