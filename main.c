#include <stdio.h>
#include <stdlib.h>
#include "uthash.h"
#include "utils.h"

typedef struct{
	int id;
	int min;	//Prob. of beating a score <= min is 100%.
	int max;	//Prob. of beating a score >= max is 0%.
	double* vals;
	UT_hash_handle hh;
} Dist;

double evaluate(int* dice, int cat, int up, int* cats, int cats_size, int* new_code){
    // ASSERT: size is the cats_size of array that cats points to.
    // ASSERT: problematic parameters won't be used. If you see "Segmentation Fault", that's probably your fault.

    // Initialization
    double score = 0.0;

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
     if (yahtzee(dice, up) > 0){
        // In the case of Yahtzee is filled:
        if ((contains(cats, 0, cats_size) >= 0) || (contains(cats, -1, cats_size) >= 0)){
            // If Yahtzee is filled with 50, get a bonus of 100.
            if (contains(cats, 0, cats_size) >= 0){
                score += 100;
            }

            // Check Joker.
            // If the corresponding upper section is filled, Joker is allowed.
            if (contains(cats, dice[0], cats_size) >= 0){
                // Check small straight, large straight, fullhouse.
                if (cat == 9){
                    score += 25;
                }else if (cat == 10){
                    score += 30;
                }else if (cat == 11){
                    score += 40;
                }
            }
        }
     }

    int* new_cats = append(cats, cat, cats_size);
    *new_code = code(new_cats, up, cats_size+1);
    free(new_cats);
    return score;
}

double prob(Dist dist, int s){
	if (s <= dist.min){
		return 1.0;
	}else if (s >= dist.max){
		return 0.0;
	}else{
		return dist.vals[s - dist.min - 1];
	}
}

double* doubleStorage(double* original, int size){
	double* result = calloc(size*2, sizeof(double));
	for (int i=0; i<size; i++){
		result[i] = original[i];
	}
	free(original);
	return result;
}

void freeDist(Dist d){
	free(d.vals);
	return;
}

Dist* expectation(int*** cache, int* empty, int up, int* cats, int cats_size, Dist* dictionary){
    int cache_sizes[] = {1,6,21,56,126,252};
    int cache_indexes[] = {0,1,7,28,84,210};
   	int min = 0;
   	int buffer_size = 50;
   	if (contains(empty, 12, 13 - cats_size) >= 0){
   		min = 5;
   	}

    Dist R3[252];
    // Evaluate R3
    for(int i=0; i<252; i++){
        int* d = cache[5][i];
        int s = min;
        int new_code = 0;
        double pr = 1.0;
        Dist dist;
        double* buffer = malloc(buffer_size*sizeof(double));

        while (pr >= 1.0){
        	double max_pr = 0.0;
	        for (int j=0; j<(13 - cats_size); j++){
	        	double score = evaluate(d,empty[j],up,cats,cats_size,&new_code);
	        	
	        	Dist* next;
	        	HASH_FIND_INT(dictionary, &new_code, next);
	        	
	        	double p = prob(*next, s - score);
	        	if (p > max_pr){
	        		max_pr = p;
	        	}
	        }
	        pr = max_pr;

	        s++;
        }
        dist.min = s-2;
        int this_min = s-2;

        while (pr > 0.0){
        	buffer[s - this_min - 2] = pr;
        	double max_pr = 0.0;
	        for (int j=0; j<(13 - cats_size); j++){
	        	double score = evaluate(d,empty[j],up,cats,cats_size,&new_code);
	        	
	        	Dist* next;
	        	HASH_FIND_INT(dictionary, &new_code, next);
	        	
	        	double p = prob(*next, s - score);
	        	if (p > max_pr){
	        		max_pr = p;
	        	}
	        }
	        pr = max_pr;
	        s++;
        }

        dist.max = s - 1;
        double* vals;
        if (s - 1 == this_min){
        	vals = NULL;
        }else{
        	vals = malloc(sizeof(double) * (s - this_min - 1));
        	for (int j=0; j<s - this_min - 1; j++){
        		vals[j] = buffer[j];
        	}
        }
        dist.vals = vals;
        R3[i] = dist;
        free(buffer);
    } 

    // Evaluate K2
    Dist K2[462];
    for (int i=0; i<252; i++){
    	K2[210+i] = R3[i];
    	K2[210+i].vals = malloc(sizeof(double)*(R3[i].max - R3[i].min - 1));
    	for (int j=0; j<R3[i].max - R3[i].min - 1; j++){
    		K2[210+i].vals[j] = R3[i].vals[j];
    	}
    }

    for (int k=4; k>=0; k = k-1){
    	for (int i=0; i<cache_sizes[k]; i++){
    		double* buffer = malloc(buffer_size*sizeof(double));
			int s = min;
    		double pr = 1.0;
    		Dist dist;
    		
    		while(pr >= 1.0){
    			double exp_pr = 0.0;
    			for (int e=1; e<7; e++){
    				int* new_d = extendDice(cache[k][i],e,k);
    				exp_pr += prob(K2[cache_indexes[k+1] + find(cache[k+1], new_d, k+1, cache_sizes[k+1])], s);
    				free(new_d);
    			}
    			pr = exp_pr / 6;
    			s++;
    		}
    		dist.min = s-2;
    		int this_min = s-2;

    		while (pr > 0.0){
    			buffer[s - this_min - 2] = pr;
    			double exp_pr = 0.0;
    			for (int e=1; e<7; e++){
    				int* new_d = extendDice(cache[k][i],e,k);
    				exp_pr += prob(K2[cache_indexes[k+1] + find(cache[k+1], new_d, k+1, cache_sizes[k+1])], s);
    				free(new_d);
    			}
    			pr = exp_pr / 6;
    			s++;
    		}

    		dist.max = s - 1;
        	double* vals;
        	if (s - 1 == this_min){
	            vals = NULL;
	        }else{
	            vals = malloc(sizeof(double) * (s - this_min - 1));
	            for (int j=0; j<s - this_min - 1; j++){
	                vals[j] = buffer[j];
	            }
	        }
	        dist.vals = vals;
    		K2[cache_indexes[k]+i] = dist;
    		free(buffer);
    	}
    }

    for (int i=0; i<1; i++){
    	printf("%d [min:%d, max%d], dist: [", i, K2[i].min, K2[i].max);
    	for (int j=0; j<K2[i].max - K2[i].min - 1; j++){
    		printf("%.6f ", K2[i].vals[j]);
    	}
    	printf("]\n");
    }


    // Free useless arrays in distributions 
    for (int i=0; i<252; i++){
    	freeDist(R3[i]);
    }

    
    for (int i=0; i<462; i++){
    	freeDist(K2[i]);
    }
    
    
    return NULL;

}

int main(){
    // Initializations
    int** cache[6];
    Dist* dictionary = NULL;
    int acc=0, choose_size[] = {1,14,90,352,935,1782,2508,2640,2079,1210,506,144,25};
    int full[] = {12,11,10,9,8,7,6,5,4,3,2,1,0};
    int cats[] = {12,11,10,9,8,7,6,5,4,3,2,-1}, empty[] = {1};
    for(int i=0; i<6; i++){
        cache[i] = dicePatterns(i);
    }
    Dist* bot = malloc(sizeof(Dist));
    bot->id = -1;
    bot->min = 0;
    bot->max = 1;
    double p[] = {};
    bot->vals = p;
    HASH_ADD_INT( dictionary, id, bot);

    /*
    Dist* result = malloc(sizeof(Dist));
    int k = -1;
    HASH_FIND_INT( dictionary, &k, result);
    printf("%d\n", result->max);
	*/

    Dist* s = expectation(cache, empty, 0, cats, 12, dictionary);

    return 0;
}

