/*
  # Enhance policy_analogs table for historical analysis

  1. Changes
    - Add `risk_factors` column (text array)
    - Add `outcome_analysis` column (text)
    - Add `policy_type` column (text)
    - Add `jurisdiction` column (text)
    - Add `time_period` column (text)
  2. Security
    - Maintain existing RLS policies
*/

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'policy_analogs' AND column_name = 'risk_factors'
  ) THEN
    ALTER TABLE policy_analogs ADD COLUMN risk_factors TEXT[];
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'policy_analogs' AND column_name = 'outcome_analysis'
  ) THEN
    ALTER TABLE policy_analogs ADD COLUMN outcome_analysis TEXT;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'policy_analogs' AND column_name = 'policy_type'
  ) THEN
    ALTER TABLE policy_analogs ADD COLUMN policy_type TEXT;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'policy_analogs' AND column_name = 'jurisdiction'
  ) THEN
    ALTER TABLE policy_analogs ADD COLUMN jurisdiction TEXT;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'policy_analogs' AND column_name = 'time_period'
  ) THEN
    ALTER TABLE policy_analogs ADD COLUMN time_period TEXT;
  END IF;
END $$;
