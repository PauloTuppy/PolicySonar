/*
  # Add created_by column to policy_analogs

  1. Changes
    - Add `created_by` column to `policy_analogs` table
  2. Security
    - Update RLS policy to include created_by check
*/

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'policy_analogs' AND column_name = 'created_by'
  ) THEN
    ALTER TABLE policy_analogs ADD COLUMN created_by UUID REFERENCES auth.users(id);
  END IF;
END $$;

CREATE OR REPLACE POLICY "Enable read access for authenticated users" 
  ON policy_analogs
  FOR SELECT
  TO authenticated
  USING (auth.uid() = created_by);
