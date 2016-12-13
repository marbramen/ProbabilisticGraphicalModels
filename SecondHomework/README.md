
Part 1 
Execute:
 	python P1_gen_rare.py gene.train > gene_RARE.train
	python count_freqs.py gene_RARE.train > gene.count
	python P1_emission_tag.py gene.dev > gene_dev.p1.out
	python eval_gene_tagger.py gene.key gene_dev.p1.out
		Found 2669 GENEs. Expected 642 GENEs; Correct: 424.

				 precision 	recall 		F1-Score
		GENE:	 0.158861	0.660436	0.256116

Part 2
Execute:
	python P2_vitterbi.py gene.count gene.dev 0 > gene_dev.p2.out
	python eval_gene_tagger.py gene.key gene_dev.p2.out
		Found 373 GENEs. Expected 642 GENEs; Correct: 202.

				precision 	recall 		F1-Score
		GENE:	 0.541555	0.314642	0.398030
	
Part 3
Execute:
	python P3_gen_new_classes.py gene.train > gene_4CLASS.trai
	python count_freqs.py gene_4CLASS.train > gene_4CLASS.count
	python P2_vitterbi.py gene_4CLASS.count gene.dev 1 > gene_dev.p3.out
	python eval_gene_tagger.py gene.key gene_dev.p3.out 
		Found 404 GENEs. Expected 642 GENEs; Correct: 219.

			 	precision 	recall 		F1-Score
		GENE:	 0.542079	0.341121	0.418738





