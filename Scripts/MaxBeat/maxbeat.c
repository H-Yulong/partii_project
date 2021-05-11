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

// Evaluates the score gained by filling a dice pattern in a given category under a gamestate.
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

// The probability of beating score s with given Dist.
double prob(Dist dist, int s){
	if (s <= dist.min){
		return 1.0;
	}else if (s >= dist.max){
		return 0.0;
	}else{
		return dist.vals[s - dist.min - 1];
	}
}

// Doubles the size of given array.
double* doubleStorage(double* original, int size){
	double* result = calloc(size*2, sizeof(double));
	for (int i=0; i<size; i++){
		result[i] = original[i];
	}
	free(original);
	return result;
}

// Deep copy a Dist.
Dist copyDist(Dist d){
	Dist result;
	result.min = d.min;
	result.max = d.max;
	result.vals = malloc(sizeof(double)*(d.max - d.min - 1));
	for (int i=0; i<d.max - d.min - 1; i++){
    		result.vals[i] = d.vals[i];
    }
    return result;
}

// Free Dist structure.
void freeDist(Dist d){
	free(d.vals);
	return;
}

// Prettyprint Dist data.
void printDist(Dist d){
	printf("min:%d, max:%d, vals:[", d.min, d.max);
    for(int i=0; i<d.max - d.min - 1; i++){
    	printf("%.15f ", d.vals[i]);
    }
    printf("]\n");

}

// Evaluates the expected score of a gamestate.
Dist expectation(int*** cache, int* empty, int up, int* cats, int cats_size, Dist* dictionary){
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
        	if (s - this_min - 2 >= buffer_size){
        		buffer = doubleStorage(buffer,buffer_size);
        		buffer_size = buffer_size*2;
        	}
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
        if (dist.max - 1 == this_min){
        	vals = NULL;
        }else{
        	vals = malloc(sizeof(double) * (dist.max - this_min - 1));
        	for (int j=0; j<dist.max - this_min - 1; j++){
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
    	K2[210+i] = copyDist(R3[i]);
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
    			if (s - this_min - 2 >= buffer_size){
	        		buffer = doubleStorage(buffer,buffer_size);
	        		buffer_size = buffer_size*2;
	        	}
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
        	if (dist.max - 1 == this_min){
	            vals = NULL;
	        }else{
	            vals = malloc(sizeof(double) * (dist.max - this_min - 1));
	            for (int j=0; j<dist.max - this_min - 1; j++){
	                vals[j] = buffer[j];
	            }
	        }
	        dist.vals = vals;
    		K2[cache_indexes[k]+i] = dist;
    		free(buffer);
    	}
    }

    // Evaluate R2
    Dist R2[462];
    R2[0] = copyDist(K2[0]);

    for (int k=1; k<6; k++){
    	for(int j=0; j<cache_sizes[k]; j++){
    		double* buffer = malloc(buffer_size*sizeof(double));
    		int s = min;
    		double pr = 1.0;
    		Dist dist;

    		while(pr >= 1.0){
    			double max_pr = prob(K2[cache_indexes[k] + j], s);
    			for (int e=1; e<7; e++){
    				int* r = removeDice(cache[k][j], e, k);
    				if (r != NULL){
	    				double val = prob(R2[cache_indexes[k-1] + find(cache[k-1], r, k-1, cache_sizes[k-1])], s);
	    				if (val > max_pr){
	    					max_pr = val;
	    				}
	    			}
    				free(r);
    			}
    			pr = max_pr;

    			s++;
    		}

    		dist.min = s-2;
    		
    		while (pr > 0.0){
    			if (s - dist.min - 2 >= buffer_size){
	        		buffer = doubleStorage(buffer,buffer_size);
	        		buffer_size = buffer_size*2;
	        	}
    			buffer[s - dist.min - 2] = pr;
    			double max_pr = prob(K2[cache_indexes[k] + j], s);
    			for (int e=1; e<7; e++){
    				int* r = removeDice(cache[k][j], e, k);
    				if (r != NULL){
	    				double val = prob(R2[cache_indexes[k-1] + find(cache[k-1], r, k-1, cache_sizes[k-1])], s);
	    				if (val > max_pr){
	    					max_pr = val;
	    				}
	    			}
    				free(r);
    			}
    			pr = max_pr;
    			s++;
    		}

    		dist.max = s - 1;
        	double* vals;
        	if (dist.max - 1 == dist.min){
	            vals = NULL;
	        }else{
	            vals = malloc(sizeof(double) * (dist.max - dist.min - 1));
	            for (int i=0; i<dist.max - dist.min - 1; i++){
	                vals[i] = buffer[i];
	            }
	        }

	        dist.vals = vals;
    		R2[cache_indexes[k]+j] = dist;
    		free(buffer);
    	}    	
    }

    // Evaluate K1
    Dist K1[462];
    for (int i=0; i<252; i++){
    	K1[210+i] = copyDist(R2[210+i]);
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
    				exp_pr += prob(K1[cache_indexes[k+1] + find(cache[k+1], new_d, k+1, cache_sizes[k+1])], s);
    				free(new_d);
    			}
    			pr = exp_pr / 6;
    			s++;
    		}
    		dist.min = s-2;
    		int this_min = s-2;

    		while (pr > 0.0){
    			if (s - this_min - 2 >= buffer_size){
	        		buffer = doubleStorage(buffer,buffer_size);
	        		buffer_size = buffer_size*2;
	        	}
    			buffer[s - this_min - 2] = pr;
    			double exp_pr = 0.0;
    			for (int e=1; e<7; e++){
    				int* new_d = extendDice(cache[k][i],e,k);
    				exp_pr += prob(K1[cache_indexes[k+1] + find(cache[k+1], new_d, k+1, cache_sizes[k+1])], s);
    				free(new_d);
    			}
    			pr = exp_pr / 6;
    			s++;
    		}

    		dist.max = s - 1;
        	double* vals;
        	if (dist.max - 1 == this_min){
	            vals = NULL;
	        }else{
	            vals = malloc(sizeof(double) * (dist.max - this_min - 1));
	            for (int j=0; j<dist.max - this_min - 1; j++){
	                vals[j] = buffer[j];
	            }
	        }
	        dist.vals = vals;
    		K1[cache_indexes[k]+i] = dist;
    		free(buffer);
    	}
    }

    // Evaluate R1
    Dist R1[462];
    R1[0] = copyDist(K1[0]);

    for (int k=1; k<6; k++){
    	for(int j=0; j<cache_sizes[k]; j++){
    		double* buffer = malloc(buffer_size*sizeof(double));
    		int s = min;
    		double pr = 1.0;
    		Dist dist;

    		while(pr >= 1.0){
    			double max_pr = prob(K1[cache_indexes[k] + j], s);
    			for (int e=1; e<7; e++){
    				int* r = removeDice(cache[k][j], e, k);
    				if (r != NULL){
	    				double val = prob(R1[cache_indexes[k-1] + find(cache[k-1], r, k-1, cache_sizes[k-1])], s);
	    				if (val > max_pr){
	    					max_pr = val;
	    				}
	    			}
    				free(r);
    			}
    			pr = max_pr;
    			s++;
    		}

    		dist.min = s-2;
    		int this_min = s-2;
    		
    		while (pr > 0.0){
    			if (s - this_min - 2 >= buffer_size){
	        		buffer = doubleStorage(buffer,buffer_size);
	        		buffer_size = buffer_size*2;
	        	}
    			buffer[s - this_min - 2] = pr;
    			double max_pr = prob(K1[cache_indexes[k] + j], s);
    			for (int e=1; e<7; e++){
    				int* r = removeDice(cache[k][j], e, k);
    				if (r != NULL){
	    				double val = prob(R1[cache_indexes[k-1] + find(cache[k-1], r, k-1, cache_sizes[k-1])], s);
	    				if (val > max_pr){
	    					max_pr = val;
	    				}
	    			}
    				free(r);
    			}
    			pr = max_pr;
    			s++;
    		}

    		dist.max = s - 1;
        	double* vals;
        	if (dist.max - 1 == this_min){
	            vals = NULL;
	        }else{
	            vals = malloc(sizeof(double) * (dist.max - this_min - 1));
	            for (int i=0; i<dist.max - this_min - 1; i++){
	                vals[i] = buffer[i];
	            }
	        }

	        dist.vals = vals;
    		R1[cache_indexes[k]+j] = dist;
    		free(buffer);
    	}    	
    }

    // Weighted Sum Operation
    // for distributation of this state
    Dist result;
    result.min = min;
    int max = min+1;
    double* buffer = calloc(buffer_size, sizeof(double));
    for(int i=0; i<252; i++){
    	double pr = prRoll(cache[5][i]);
    	Dist d = R1[210+i];
    	if (d.max > max){
    		max = d.max;
    	}
    	if (max - min - 1 > buffer_size){
    		buffer = doubleStorage(buffer,buffer_size);
    		buffer_size = buffer_size * 2;
    	}
    	for (int j=0; j<d.max - min - 1; j++){
    		buffer[j] += prob(d,min + j + 1)*pr;
    	}
    }
    result.max = max;
    result.vals = malloc(sizeof(double) * (result.max - result.min - 1));
    for(int i=0; i<result.max - result.min - 1; i++){
    	result.vals[i] = buffer[i];
    }
   
    //printDist(result);
	/*
    Dist* var = R1;
    for (int i=210; i<462; i++){
    	printf("%d [min:%d, max%d], dist: [", i, var[i].min, var[i].max);
    	for (int j=0; j<var[i].max - var[i].min - 1; j++){
    		printf("%.6f ", var[i].vals[j]);
    	}
    	printf("]\n");
    }
	//*/

    // Free useless arrays in distributions 
    for (int i=0; i<252; i++){
    	freeDist(R3[i]);
    }

    
    for (int i=0; i<462; i++){
    	freeDist(K2[i]);
    	freeDist(R2[i]);
    	freeDist(K1[i]);
    	freeDist(R1[i]);
    }
    
    
    return result;

}

int main(){
    // Initializations
    int** cache[6];
    for(int i=0; i<6; i++){
        cache[i] = dicePatterns(i);
    }

    Dist* dictionary = NULL;
    int acc=0, choose_size[] = {1,14,90,352,935,1782,2508,2640,2079,1210,506,144,25};
    int full[] = {12,11,10,9,8,7,6,5,4,3,2,1,0};
    //int cats[] = {11,10,9,8,7,6,5,4,3,2,1,-1}, empty[] = {12};
    int cats_size = 0;

    ///*
    // Clear output files
    FILE* fp1 = fopen("D:\\Prog\\partii_project\\Table_Maximize\\13","w");
	FILE* fp2 = fopen("D:\\Prog\\partii_project\\Table_Maximize\\13_readbale.txt","w");
	fclose(fp1);
	fclose(fp2);
    //*/

    ///*
    // Loading
    FILE* fpsource = fopen("D:\\Prog\\partii_project\\Table_Maximize\\12","rb");

    printf("Loading...\n");
    int buffer = 0;
    while(fread(&buffer, sizeof(int), 1, fpsource) == 1){

    	Dist* dist = malloc(sizeof(Dist));

    	// Read id
    	dist->id = buffer;
        //printf("%d\n",buffer);

    	// Read min,max
    	fread(&buffer, sizeof(int), 1, fpsource);
    	dist->min = buffer;
    	fread(&buffer, sizeof(int), 1, fpsource);
    	dist->max = buffer;
        //printf("%d\n",dist->min);
        //printf("%d\n",dist->max);

    	
    	// Read vals
        double* vals;
        if ((dist->max - dist->min - 1) > 0){
            vals = malloc(sizeof(double) * (dist->max - dist->min - 1));
        }else{
            vals = NULL;
        }


        double dbuffer;
        fread(vals, sizeof(double), dist->max - dist->min - 1, fpsource);
        /*
        for(int i=0; i<(dist->max - dist->min - 1); i++){
            printf("%f\n", vals[i]);
        }
        //*/
        
        dist->vals = vals;
        HASH_ADD_INT(dictionary, id, dist);
        //return 0;

    }
    fclose(fpsource);
    //*/ 

 
    //printDist(expectation(cache, empty, 0, cats, 12, dictionary));
    
    ///*
    // Calculations
    int** states = choosePatterns(cats_size);
    for (int j=0; j<choose_size[cats_size]; j++){
		int empty[13-cats_size];
		int p=0;
		for(int k=0; k<12; k++){
			if (contains(states[j],full[k],cats_size) < 0){
				empty[p++] = full[k];
			}
		}

		if ((contains(states[j],0,cats_size) < 0) && (contains(states[j],-1,cats_size) < 0)){
			empty[p++] = 0;
		}

		for (int u=0; u<64; u++){
            
			FILE* fp1 = fopen("D:\\Prog\\partii_project\\Table_Maximize\\13","ab");
			FILE* fp2 = fopen("D:\\Prog\\partii_project\\Table_Maximize\\13_readbale.txt","a");
			Dist d = expectation(cache, empty, u, states[j], cats_size, dictionary);
			//printDist(d);
			
			// Output code
			int c = code(states[j], u, cats_size);
            fwrite(&c, sizeof(int), 1, fp1);
			fprintf(fp2, "%d\n", c);

			// Outout min,max
            fwrite(&d.min, sizeof(int), 1, fp1);
            fwrite(&d.max, sizeof(int), 1, fp1);
			fprintf(fp2, "min: %d\n", d.min);
			fprintf(fp2, "max: %d\n", d.max);

			// Output vals
            fwrite(d.vals, sizeof(double), d.max - d.min - 1, fp1);
            for(int l=0; l<d.max - d.min - 1; l++){
                fprintf(fp2, "%.6f ", d.vals[l]);
            }
            fprintf(fp2, "\n");
            
			acc++;
			printf("%d / %d\n", acc, choose_size[cats_size] * 64);
			fclose(fp1);
			fclose(fp2);
		}
	}
    //*/
    
    return 0;
}

